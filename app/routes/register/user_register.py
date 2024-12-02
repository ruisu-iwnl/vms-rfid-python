import os
from flask import Blueprint, render_template, redirect, flash, request, make_response
from ..utils.forms import UserRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import hash_password, verify_recaptcha, check_existing_registration
import mysql.connector
import uuid
import re
from ..utils.session import check_logged_in_redirect
from ..utils.cache import disable_caching, redirect_to
from werkzeug.utils import secure_filename

user_register_bp = Blueprint('user_register', __name__)

MAX_FILE_SIZE = 25 * 1024 * 1024  

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    unique_id = uuid.uuid4().hex[:8] 
    file_extension = os.path.splitext(sanitized_filename)[1]
    return f"{unique_id}{file_extension}"

@user_register_bp.route('', methods=['GET', 'POST'])
def user_register():
    print("Handling user registration request.")

    response = check_logged_in_redirect()
    if response:
        print("User is already logged in. Redirecting...")
        return response

    form = UserRegisterForm()
    recaptcha_error = None
    duplicate_entry_error = None
    is_registered_as_user = None
    is_registered_as_admin = None
    rfid_already_registered = None
    email_already_registered = None

    PROFILE_IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images', 'users')

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

                # Check if email is already registered
                cursor, connection = get_cursor()
                cursor.execute("SELECT email FROM user WHERE BINARY email = %s", (form.email.data,))
                email_record = cursor.fetchone()
                if email_record:
                    email_already_registered = "This email is already registered. Please use a different email."

                # Check if RFID is already registered
                cursor.execute("SELECT rfid_no FROM rfid WHERE BINARY rfid_no = %s", (form.rfid_number.data,))
                rfid_record = cursor.fetchone()
                if rfid_record:
                    rfid_already_registered = "This RFID is already registered. Please use a different RFID."

                if email_already_registered or rfid_already_registered:
                    return render_template(
                        'register/user_register.html',
                        form=form,
                        recaptcha_error=recaptcha_error,
                        duplicate_entry_error=duplicate_entry_error,
                        is_registered_as_user=is_registered_as_user,
                        is_registered_as_admin=is_registered_as_admin,
                        email_already_registered=email_already_registered,
                        rfid_already_registered=rfid_already_registered
                    )

                # Proceed with user creation (remaining logic)
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

                # Insert into passwords table
                password_query = """
                    INSERT INTO passwords (password_hash) 
                    VALUES (%s)
                """
                cursor.execute(password_query, (hashed_password,))
                connection.commit()

                # Get the password_id
                cursor.execute("SELECT LAST_INSERT_ID()")
                password_id = cursor.fetchone()[0]

                # Insert user data
                query = """
                    INSERT INTO user (emp_no, lastname, firstname, email, contactnumber, password_id, profile_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    form.employeenumber.data,
                    form.lastname.data,
                    form.firstname.data,
                    form.email.data,
                    form.contactnumber.data,
                    password_id,
                    profile_image_filename
                )
                cursor.execute(query, values)
                connection.commit()

                # Get user ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                user_id = cursor.fetchone()[0]

                # Insert RFID
                rfid_query = """
                    INSERT INTO rfid (rfid_no) 
                    VALUES (%s)
                """
                cursor.execute(rfid_query, (form.rfid_number.data,))
                connection.commit()

                # Insert vehicle
                vehicle_query = """
                    INSERT INTO vehicle (user_id, licenseplate, make, model, rfid_no)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(vehicle_query, (user_id, form.license_plate.data, form.make.data, form.model.data, form.rfid_number.data))
                connection.commit()

                cursor.close()
                close_db_connection(connection)
                print("Database connection closed.")

                flash("Registration successful", "success")
                return redirect_to('login.login')

            except mysql.connector.IntegrityError as e:
                print(f"Database error: {e}")
                duplicate_entry_error = "A database error occurred. Please try again."
                response = make_response(render_template(
                    'register/user_register.html',
                    form=form,
                    recaptcha_error=recaptcha_error,
                    duplicate_entry_error=duplicate_entry_error
                ))
                response = disable_caching(response)
                return response

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", "danger")
                response = make_response(render_template(
                    'register/user_register.html',
                    form=form,
                    recaptcha_error=recaptcha_error
                ))
                response = disable_caching(response)
                return response

    response = make_response(render_template(
        'register/user_register.html',
        form=form,
        recaptcha_error=recaptcha_error,
        duplicate_entry_error=duplicate_entry_error
    ))
    response = disable_caching(response)
    return response
