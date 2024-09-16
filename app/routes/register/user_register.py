from flask import Blueprint, render_template, redirect, flash, request, make_response
from ..utils.forms import UserRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import hash_password, verify_recaptcha, check_existing_registration
import mysql.connector
from ..utils.session import check_logged_in_redirect
from ..utils.cache import disable_caching, redirect_to

user_register_bp = Blueprint('user_register', __name__)

@user_register_bp.route('', methods=['GET', 'POST'])
def user_register():
    response = check_logged_in_redirect()
    if response:
        return response

    form = UserRegisterForm()
    recaptcha_error = None
    duplicate_entry_error = None
    is_registered_as_user = None
    is_registered_as_admin = None

    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
            print("reCAPTCHA verification failed.")

        else:
            try:
                print("reCAPTCHA verified. Proceeding with registration.")

                # Check if email is already registered as a user or admin
                is_registered_as_user, is_registered_as_admin = check_existing_registration(form.email.data)

                if is_registered_as_user:
                    flash("This email is already registered as a user.", "danger")
                    return render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, is_registered_as_user="This email is already registered as a user.")

                if is_registered_as_admin:
                    flash("This email is already registered as an admin. Cannot register as a user with the same email.", "danger")
                    return render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, is_registered_as_admin="This email is already registered as an admin. Cannot register as a user with the same email.")

                # If not registered as user or admin, proceed with registration
                cursor, connection = get_cursor()
                print("Database cursor and connection obtained.")
                hashed_password = hash_password(form.password.data)
                print(f"Hashed password: {hashed_password}")

                query = """
                    INSERT INTO user (emp_no, lastname, firstname, email, contactnumber, password)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    form.employeenumber.data,
                    form.lastname.data,
                    form.firstname.data,
                    form.email.data,
                    form.contactnumber.data,
                    hashed_password
                )
                print(f"Executing query with values: {values}")
                cursor.execute(query, values)
                connection.commit()
                print("Data committed to the database.")
                cursor.close()
                close_db_connection(connection)

                flash("Registration successful", "success")
                return redirect_to('user_login.user_login')

            except mysql.connector.IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry error code
                    duplicate_entry_error = "An employee with this number already exists. Please use a different number."
                else:
                    flash(f"Database error: {e}", "danger")
                response = make_response(render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
                response = disable_caching(response)
                return response

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", "danger")
                response = make_response(render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
                response = disable_caching(response)
                return response

    response = make_response(render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error, is_registered_as_user=is_registered_as_user, is_registered_as_admin=is_registered_as_admin))
    response = disable_caching(response)
    return response
