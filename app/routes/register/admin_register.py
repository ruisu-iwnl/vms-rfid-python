from flask import Blueprint, render_template, redirect, flash, request, make_response
from ..utils.forms import AdminRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import hash_password, verify_recaptcha, check_existing_registration
import mysql.connector
import os
from werkzeug.utils import secure_filename
import uuid
import re
from ..utils.session import check_logged_in_redirect
from ..utils.cache import disable_caching, redirect_to

admin_register_bp = Blueprint('admin_register', __name__)

MAX_FILE_SIZE = 25 * 1024 * 1024  

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    unique_id = uuid.uuid4().hex[:8] 
    file_extension = os.path.splitext(sanitized_filename)[1]
    return f"{unique_id}{file_extension}"

@admin_register_bp.route('', methods=['GET', 'POST'])
def admin_register():
    print("Handling admin registration request.")

    response = check_logged_in_redirect()
    if response:
        print("Admin is already logged in. Redirecting...")
        return response

    form = AdminRegisterForm()
    recaptcha_error = None
    duplicate_entry_error = None
    is_registered_as_user = None
    is_registered_as_admin = None

    PROFILE_IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images', 'admins')

    if not os.path.exists(PROFILE_IMAGE_FOLDER):
        os.makedirs(PROFILE_IMAGE_FOLDER)

    if form.validate_on_submit():
        print("Form validated on submit. Proceeding with registration.")
        recaptcha_response = request.form.get('g-recaptcha-response')
        print(f"Received reCAPTCHA response: {recaptcha_response}")

        if not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
            print("reCAPTCHA verification failed.")
        else:
            try:
                print("reCAPTCHA verified. Proceeding with registration.")

                is_registered_as_user, is_registered_as_admin = check_existing_registration(form.email.data)

                if is_registered_as_user:
                    is_registered_as_user = "This email is already registered as a user. Cannot register as an admin with the same email."
                if is_registered_as_admin:
                    is_registered_as_admin = "This email is already registered as an admin."

                if is_registered_as_user or is_registered_as_admin:
                    return render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin)

                cursor, connection = get_cursor()
                print("Database cursor and connection obtained.")

                profile_image_filename = None
                profile_image = request.files.get('profile_image')
                
                if profile_image and profile_image.mimetype.startswith('image/') and profile_image.content_length <= MAX_FILE_SIZE:
                    profile_image_filename = secure_filename(profile_image.filename)
                    profile_image_filename = sanitize_filename(profile_image_filename)
                    image_path = os.path.join(PROFILE_IMAGE_FOLDER, profile_image_filename)
                    profile_image.save(image_path)
                    print(f"Image saved at {image_path}")
                elif profile_image:
                    if not profile_image.mimetype.startswith('image/'):
                        flash("Invalid file type. Please upload an image file.", 'danger')
                    else:
                        flash("Image file is too large. Please upload an image under 25 MB.", 'danger')
                    return redirect(request.url)

                hashed_password = hash_password(form.password.data)
                print(f"Hashed password: {hashed_password}")

                query = """
                    INSERT INTO admin (employee_id, lastname, firstname, email, contactnumber, password, profile_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    form.employeenumber.data,
                    form.lastname.data,
                    form.firstname.data,
                    form.email.data,
                    form.contactnumber.data,
                    hashed_password,
                    profile_image_filename 
                )
                print(f"Executing query with values: {values}")

                cursor.execute(query, values)
                connection.commit()
                print("Data committed to the database.")

                cursor.close()
                close_db_connection(connection)
                print("Database connection closed.")

                flash("Registration successful", "success")
                return redirect_to('login.login')

            except mysql.connector.IntegrityError as e:
                print(f"Database error: {e}")
                if e.args[0] == 1062: 
                    duplicate_entry_error = "An admin with this employee ID already exists. Please use a different ID."
                else:
                    flash(f"Database error: {e}", "danger")
                response = make_response(render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
                response = disable_caching(response)
                return response

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", "danger")
                response = make_response(render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
                response = disable_caching(response)
                return response

    print("Rendering registration form.")
    response = make_response(render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
    response = disable_caching(response)
    return response
