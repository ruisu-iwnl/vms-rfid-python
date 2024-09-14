from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..utils.forms import AdminRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import hash_password, verify_recaptcha
import mysql.connector
from ..utils.session import check_logged_in_redirect

admin_register_bp = Blueprint('admin_register', __name__)

@admin_register_bp.route('', methods=['GET', 'POST'])
def admin_register():
    
    response = check_logged_in_redirect()
    if response:
        return response


    form = AdminRegisterForm()
    recaptcha_error = None
    duplicate_entry_error = None

    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        if not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
        else:
            try:
                print("reCAPTCHA verified. Proceeding with registration.")

                cursor, connection = get_cursor()

                hashed_password = hash_password(form.password.data)

                query = """
                    INSERT INTO admin (employee_id, lastname, firstname, email, contactnumber, password)
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

                cursor.execute(query, values)
                connection.commit()

                cursor.close()
                close_db_connection(connection)

                flash("Registration successful", "success")
                return redirect(url_for('admin_login.admin_login'))

            except mysql.connector.IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry error code
                    duplicate_entry_error = "An admin with this employee ID already exists. Please use a different ID."
                else:
                    flash(f"Database error: {e}", "danger")
                return render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", "danger")
                return render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)

    return render_template('register/admin_register.html', form=form, recaptcha_error=recaptcha_error, duplicate_entry_error=duplicate_entry_error)
