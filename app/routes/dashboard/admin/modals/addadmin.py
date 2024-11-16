import os
from flask import Blueprint, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.forms import AddAdminForm
from app.routes.utils.utils import check_existing_registration
from app.routes.utils.activity_log import log_login_activity  
import mysql.connector

addadmin_bp = Blueprint('addadmin', __name__)

MAX_FILE_SIZE = 25 * 1024 * 1024

@addadmin_bp.route('/admin/addadmin', methods=['GET', 'POST'])
def add_admin():
    print("Entering add_admin route")
    
    admin_id = session.get('admin_id')
    if not admin_id:
        flash('Admin session not found. Please log in again.', 'error')
        return redirect(url_for('main.index'))

    form = AddAdminForm()
    
    if form.validate_on_submit():
        emp_no = form.employeenumber.data
        lastname = form.lastname.data
        firstname = form.firstname.data
        email = form.email.data
        contactnumber = form.contactnumber.data
        password = form.password.data

        filename = None
        profile_image = request.files.get('profile_image')
        
        if profile_image and profile_image.mimetype.startswith('image/') and profile_image.content_length <= MAX_FILE_SIZE:
            filename = secure_filename(profile_image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'admins')
            os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
            image_path = os.path.join(upload_folder, filename)
            profile_image.save(image_path)
            print(f"Image saved at {image_path}")
        elif profile_image:
            if not profile_image.mimetype.startswith('image/'):
                flash("Invalid file type. Please upload an image file.", 'danger')
            else:
                flash("Image file is too large. Please upload an image under 25 MB.", 'danger')
            return redirect(url_for('adminlist.adminlist', page=1, sort_by='emp_no', order='asc'))

        hashed_password = generate_password_hash(password)
        try:
            is_registered_as_user, is_registered_as_admin = check_existing_registration(email)
            if is_registered_as_user or is_registered_as_admin:
                flash("This email is already registered.", "danger")
                return redirect(url_for('adminlist.adminlist', page=1, sort_by='emp_no', order='asc'))

            cursor, connection = get_cursor()
            cursor.execute("""
                INSERT INTO admin (employee_id, lastname, firstname, email, contactnumber, password, profile_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (emp_no, lastname, firstname, email, contactnumber, hashed_password, filename))
            connection.commit()

            flash('Admin added successfully.', 'success')
            log_login_activity(admin_id, 'Admin', 'Added new admin')

            return redirect(url_for('adminlist.adminlist', page=1, sort_by='emp_no', order='asc'))
        except mysql.connector.IntegrityError:
            flash("Database error: could not add admin.", "danger")
        finally:
            close_db_connection(connection)

    return redirect(url_for('adminlist.adminlist', page=1, sort_by='emp_no', order='asc'))
