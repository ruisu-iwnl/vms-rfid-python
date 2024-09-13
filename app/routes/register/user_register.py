from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import UserRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils import hash_password, verify_recaptcha
import mysql.connector

user_register_bp = Blueprint('user_register', __name__)

@user_register_bp.route('', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    recaptcha_error = None
    duplicate_entry_error = None

    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')
        # print(f"Received reCAPTCHA response: {recaptcha_response}")

        if not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
            # print("reCAPTCHA verification failed.")
        else:
            try:
                print("reCAPTCHA verified. Proceeding with registration.")

                cursor, connection = get_cursor()
                # print("Database cursor and connection obtained.")

                hashed_password = hash_password(form.password.data)
                # print(f"Hashed password: {hashed_password}")

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
                # print(f"Executing query with values: {values}")

                cursor.execute(query, values)
                connection.commit()
                print("Data committed to the database.")

                cursor.close()
                close_db_connection(connection)
                # print("Database connection closed.")

                flash("Registration successful", "success")
                return redirect(url_for('user_dashboard.user_dashboard'))

            except mysql.connector.IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry error code
                    duplicate_entry_error = "An employee with this number already exists. Please use a different number."
                else:
                    flash(f"Database error: {e}", "danger")
                return render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", "danger")
                return render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)

    return render_template('register/user_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)
