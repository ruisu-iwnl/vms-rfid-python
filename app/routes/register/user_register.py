import os
from flask import Blueprint, render_template, redirect, flash, request, make_response, jsonify
from ..utils.forms import UserRegisterForm
from app.models.database import get_cursor, close_db_connection, get_cars_cursor
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

@user_register_bp.route('/search_makes', methods=['GET'])
def search_makes():
    makes = set()

    try:
        cursor, connection = get_cars_cursor()
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            # print(f"Columns in {table_name}: {columns}")  # Debugging line

            if 'make' in columns:
                cursor.execute(f"SELECT DISTINCT make FROM {table_name}")
                makes_list = cursor.fetchall()
                # print(f"Fetched makes for {table_name}: {makes_list}")  # Debugging line
                for (make,) in makes_list:
                    makes.add(make)

        close_db_connection(connection)

        # Debugging: print the makes that are being returned
        print(f"Makes: {sorted(makes)}")

    except Exception as e:
        print(f"Error fetching makes: {e}")
        return jsonify({'error': str(e)}), 500

    return jsonify(sorted(makes))

@user_register_bp.route('/search_models', methods=['GET'])
def search_models():
    make = request.args.get('make', '')
    models = set()

    if not make:
        return jsonify(list(models))

    try:
        cursor, connection = get_cars_cursor()
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            # print(f"Columns in {table_name}: {columns}")  # Debugging line

            if 'make' in columns and 'model' in columns:
                cursor.execute(f"SELECT DISTINCT model FROM {table_name} WHERE make = %s", (make,))
                models_list = cursor.fetchall()
                # print(f"Fetched models for make {make} from {table_name}: {models_list}")  # Debugging line
                for (model,) in models_list:
                    models.add(model)

        close_db_connection(connection)

        # Debugging: print the models that are being returned
        # print(f"Models for {make}: {sorted(models)}")

    except Exception as e:
        print(f"Error fetching models: {e}")
        return jsonify({'error': str(e)}), 500

    return jsonify(sorted(models))

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
    emp_no_already_registered = None

    PROFILE_IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images', 'users')
    DOCUMENTS_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'documents')

    if not os.path.exists(PROFILE_IMAGE_FOLDER):
        os.makedirs(PROFILE_IMAGE_FOLDER)

    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)

    print("Profile image and documents folder setup.")

    disable_recaptcha = os.getenv('DISABLE_RECAPTCHA', 'False').lower() == 'true'

    if form.validate_on_submit():
        print("Form validated on submit. Proceeding with registration.")
        recaptcha_response = request.form.get('g-recaptcha-response')
        print(f"Received reCAPTCHA response: {recaptcha_response}")

        if not disable_recaptcha and not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
            print("reCAPTCHA verification failed.")
        else:
            try:
                print("reCAPTCHA verified. Proceeding with registration.")

                cursor, connection = get_cursor()

                # Check if email already exists, disregarding soft-deleted records
                cursor.execute("SELECT email FROM user WHERE BINARY email = %s AND deleted_at IS NULL", (form.email.data,))
                email_record = cursor.fetchone()
                print(f"Email check result: {email_record}")

                if email_record:
                    email_already_registered = "This email is already registered. Please use a different email."

                # Check if RFID already exists
                cursor.execute("SELECT rfid_no FROM rfid WHERE BINARY rfid_no = %s", (form.rfid_number.data,))
                rfid_record = cursor.fetchone()
                print(f"RFID check result: {rfid_record}")

                if rfid_record:
                    rfid_already_registered = "This RFID is already registered. Please use a different RFID."

                # Check if employee number already exists in either user or admin tables
                cursor.execute("SELECT emp_no FROM user WHERE BINARY emp_no = %s AND deleted_at IS NULL", (form.employeenumber.data,))
                user_emp_no_record = cursor.fetchone()
                if user_emp_no_record:
                    emp_no_already_registered = "This employee number is already registered as a user. Please use a different number."

                cursor.execute("SELECT employee_id FROM admin WHERE BINARY employee_id = %s AND deleted_at IS NULL", (form.employeenumber.data,))
                admin_emp_no_record = cursor.fetchone()
                if admin_emp_no_record:
                    emp_no_already_registered = "This employee number is already registered as an admin. Please use a different number."

                # If there are any registration errors, return the form with errors
                if email_already_registered or rfid_already_registered or emp_no_already_registered:
                    print("Email, RFID, or Employee number already registered, returning the form with errors.")
                    return render_template(
                        'register/user_register.html',
                        form=form,
                        recaptcha_error=recaptcha_error,
                        duplicate_entry_error=duplicate_entry_error,
                        is_registered_as_user=is_registered_as_user,
                        is_registered_as_admin=is_registered_as_admin,
                        email_already_registered=email_already_registered,
                        rfid_already_registered=rfid_already_registered,
                        emp_no_already_registered=emp_no_already_registered
                    )

                profile_image_filename = None
                profile_image = request.files.get('profile_image')

                if profile_image:
                    print(f"Received profile image: {profile_image.filename}")
                    if profile_image.mimetype.startswith('image/') and profile_image.content_length <= MAX_FILE_SIZE:
                        profile_image_filename = secure_filename(profile_image.filename)
                        profile_image_filename = sanitize_filename(profile_image_filename)
                        image_path = os.path.join(PROFILE_IMAGE_FOLDER, profile_image_filename)
                        profile_image.save(image_path)
                        print(f"Image saved at {image_path}")
                    else:
                        print("Profile image invalid or too large.")
                        if not profile_image.mimetype.startswith('image/'):
                            flash("Invalid file type. Please upload an image file.", 'danger')
                        else:
                            flash("Image file is too large. Please upload an image under 25 MB.", 'danger')
                        return redirect(request.url)

                driver_license_filename = None
                driver_license_image = request.files.get('driver_license')

                if driver_license_image:
                    print(f"Received driver's license image: {driver_license_image.filename}")
                    if driver_license_image.mimetype.startswith('image/') and driver_license_image.content_length <= MAX_FILE_SIZE:
                        driver_license_filename = secure_filename(driver_license_image.filename)
                        driver_license_filename = sanitize_filename(driver_license_filename)
                        license_image_path = os.path.join(DOCUMENTS_FOLDER, driver_license_filename)
                        driver_license_image.save(license_image_path)
                        print(f"Driver's license image saved at {license_image_path}")
                    else:
                        print("Driver's license image invalid or too large.")
                        if not driver_license_image.mimetype.startswith('image/'):
                            flash("Invalid file type for driver's license. Please upload an image file.", 'danger')
                        else:
                            flash("Driver's license file is too large. Please upload an image under 25 MB.", 'danger')
                        return redirect(request.url)

                orcr_filename = None
                orcr_image = request.files.get('orcr_image')  # Corrected field name

                if orcr_image:
                    print(f"Received ORCR image: {orcr_image.filename}")
                    if orcr_image.mimetype.startswith('image/') and orcr_image.content_length <= MAX_FILE_SIZE:
                        orcr_filename = secure_filename(orcr_image.filename)
                        orcr_filename = sanitize_filename(orcr_filename)
                        orcr_image_path = os.path.join(DOCUMENTS_FOLDER, orcr_filename)
                        orcr_image.save(orcr_image_path)
                        print(f"ORCR image saved at {orcr_image_path}")
                    else:
                        print("ORCR image invalid or too large.")
                        if not orcr_image.mimetype.startswith('image/'):
                            flash("Invalid file type for ORCR. Please upload an image file.", 'danger')
                        else:
                            flash("ORCR file is too large. Please upload an image under 25 MB.", 'danger')
                        return redirect(request.url)

                hashed_password = hash_password(form.password.data)
                print(f"Hashed password: {hashed_password}")

                password_query = """
                    INSERT INTO passwords (password_hash) 
                    VALUES (%s)
                """
                cursor.execute(password_query, (hashed_password,))
                connection.commit()
                print("Password inserted into database.")

                cursor.execute("SELECT LAST_INSERT_ID()")
                password_id = cursor.fetchone()[0]
                print(f"Retrieved password_id: {password_id}")

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
                print(f"Executing user insert with values: {values}")
                cursor.execute(query, values)
                connection.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                user_id = cursor.fetchone()[0]
                print(f"Retrieved user_id: {user_id}")

                rfid_query = """
                    INSERT INTO rfid (rfid_no) 
                    VALUES (%s)
                """
                cursor.execute(rfid_query, (form.rfid_number.data,))
                connection.commit()
                print(f"Inserted RFID {form.rfid_number.data} into database.")

                vehicle_query = """
                    INSERT INTO vehicle (user_id, licenseplate, make, model, rfid_no)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(vehicle_query, (user_id, form.license_plate.data, form.make.data, form.model.data, form.rfid_number.data))
                connection.commit()
                print("Vehicle inserted into database.")

                # Insert ORCR and driver license into user_documents table
                user_documents_query = """
                    INSERT INTO user_documents (user_id, orcr, driverlicense)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(user_documents_query, (user_id, orcr_filename, driver_license_filename))
                connection.commit()
                print("User documents inserted into database.")

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

    print("Form validation failed.")
    response = make_response(render_template(
        'register/user_register.html',
        form=form,
        recaptcha_error=recaptcha_error,
        duplicate_entry_error=duplicate_entry_error
    ))
    response = disable_caching(response)
    return response
