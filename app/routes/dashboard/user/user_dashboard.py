from flask import Blueprint, render_template, session
from app.routes.utils.session import check_access
from app.routes.dashboard.user.charts.timeinoutcompare import get_time_in_time_out_comparison
from app.routes.dashboard.user.charts.peakhours import get_peak_hours_of_vehicle_entries
from app.routes.dashboard.user.charts.durationofstay import get_vehicle_stay_durations
from app.routes.dashboard.user.charts.mostactivedays import most_active_days
from app.routes.utils.utils import get_name, get_emp_profile_info
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.forms import ProfileForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import uuid
import re

user_dashboard_bp = Blueprint('user_dashboard', __name__)

from flask import request, redirect, url_for, flash

csrf = CSRFProtect()

MAX_FILE_SIZE = 25 * 1024 * 1024  

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    unique_id = uuid.uuid4().hex[:8] 
    file_extension = os.path.splitext(sanitized_filename)[1]
    return f"{unique_id}{file_extension}"

@user_dashboard_bp.route('', methods=['GET', 'POST'])
def user_dashboard():
    response = check_access('user')
    if response:
        return response

    user_id = session['user_id']
    user_name = get_name(user_id)

    form = ProfileForm()

    PROFILE_IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'images', 'users')
    DOCUMENTS_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'documents')

    os.makedirs(PROFILE_IMAGE_FOLDER, exist_ok=True)
    os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        contactnumber = form.contactnumber.data

        # Handle profile image upload
        profile_image_filename = None
        profile_image = request.files.get('profile_image')
        if profile_image and profile_image.filename:
            if profile_image.mimetype.startswith('image/') and profile_image.content_length <= MAX_FILE_SIZE:
                profile_image_filename = secure_filename(profile_image.filename)
                profile_image_filename = sanitize_filename(profile_image_filename)
                image_path = os.path.join(PROFILE_IMAGE_FOLDER, profile_image_filename)
                profile_image.save(image_path)
            else:
                flash("Invalid or too large profile image. Please upload a valid image under 25 MB.", 'danger')
                return redirect(request.url)

        # Handle ORCR image upload
        orcr_filename = None
        orcr_image = request.files.get('orcr_image')
        if orcr_image and orcr_image.filename:
            if orcr_image.mimetype.startswith('image/') and orcr_image.content_length <= MAX_FILE_SIZE:
                orcr_filename = secure_filename(orcr_image.filename)
                orcr_filename = sanitize_filename(orcr_filename)
                orcr_image_path = os.path.join(DOCUMENTS_FOLDER, orcr_filename)
                orcr_image.save(orcr_image_path)
            else:
                flash("Invalid or too large ORCR image. Please upload a valid image under 25 MB.", 'danger')
                return redirect(request.url)

        # Handle driver license image upload
        driver_license_filename = None
        driver_license_image = request.files.get('driver_license_image')
        if driver_license_image and driver_license_image.filename:
            if driver_license_image.mimetype.startswith('image/') and driver_license_image.content_length <= MAX_FILE_SIZE:
                driver_license_filename = secure_filename(driver_license_image.filename)
                driver_license_filename = sanitize_filename(driver_license_filename)
                license_image_path = os.path.join(DOCUMENTS_FOLDER, driver_license_filename)
                driver_license_image.save(license_image_path)
            else:
                flash("Invalid or too large driver's license image. Please upload a valid image under 25 MB.", 'danger')
                return redirect(request.url)

        try:
            cursor, connection = get_cursor()

            # Check if there are any changes to update
            update_user_query = """
                UPDATE user
                SET firstname = %s, lastname = %s, email = %s, contactnumber = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
                AND (firstname != %s OR lastname != %s OR email != %s OR contactnumber != %s)
            """
            cursor.execute(update_user_query, (firstname, lastname, email, contactnumber, user_id, firstname, lastname, email, contactnumber))

            # If there were changes, update the approval status
            if cursor.rowcount > 0:
                cursor.execute("""
                    UPDATE user
                    SET is_approved = 0
                    WHERE user_id = %s
                """, (user_id,))

            # Update profile image if it was uploaded
            if profile_image_filename:
                cursor.execute("""
                    UPDATE user
                    SET profile_image = %s
                    WHERE user_id = %s
                """, (profile_image_filename, user_id))

            # Update user documents if they were uploaded
            if orcr_filename or driver_license_filename:
                cursor.execute("""
                    SELECT document_id FROM user_documents WHERE user_id = %s
                """, (user_id,))
                document_exists = cursor.fetchone()

                if document_exists:
                    cursor.execute("""
                        UPDATE user_documents
                        SET orcr = COALESCE(%s, orcr), driverlicense = COALESCE(%s, driverlicense)
                        WHERE user_id = %s
                    """, (orcr_filename, driver_license_filename, user_id))
                else:
                    cursor.execute("""
                        INSERT INTO user_documents (user_id, orcr, driverlicense)
                        VALUES (%s, %s, %s)
                    """, (user_id, orcr_filename, driver_license_filename))

            connection.commit()
            flash("Profile updated successfully!", "success")

        except Exception as e:
            print(f"Error updating profile: {e}")
            flash("An error occurred while updating the profile.", "error")

        finally:
            cursor.close()
            close_db_connection(connection)

        return redirect(url_for('user_dashboard.user_dashboard'))

    # Fetch required data for rendering the dashboard
    time_in_time_out_data = get_time_in_time_out_comparison(user_id)
    peak_hours_data = get_peak_hours_of_vehicle_entries()
    vehicle_stay_durations_data = get_vehicle_stay_durations(user_id)
    most_active_days_data = most_active_days(user_id)

    user_profile = get_emp_profile_info(user_id)

    return render_template('dashboard/user/user_dashboard.html',
                           form=form, 
                           user_name=user_name,
                           time_in_time_out_data=time_in_time_out_data,
                           peak_hours_data=peak_hours_data,
                           vehicle_stay_durations_data=vehicle_stay_durations_data,
                           most_active_days_data=most_active_days_data,
                           user=user_profile)
