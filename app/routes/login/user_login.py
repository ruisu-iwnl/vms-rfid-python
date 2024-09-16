from flask import Blueprint, render_template, redirect, url_for, flash, session, request, make_response
from ..utils.forms import BaseLoginForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import verify_password, verify_recaptcha
from ..utils.session import check_logged_in_redirect
from ..utils.cache import disable_caching, redirect_to

user_login_bp = Blueprint('user_login', __name__)

@user_login_bp.route('', methods=['GET', 'POST'])
def user_login():
    print(f"Session before login attempt: {session}")

    response = check_logged_in_redirect()
    if response:
        return response

    form = BaseLoginForm()
    recaptcha_error = None
    login_error = None

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        print(f"Form submitted. Email: {email}, Password: [PROTECTED]")

        recaptcha_response = request.form.get('g-recaptcha-response')
        print(f"Received reCAPTCHA response: {recaptcha_response}")

        if not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
            print("reCAPTCHA verification failed.")
        else:
            try:
                print("reCAPTCHA verified. Proceeding with login.")

                cursor, connection = get_cursor()
                print("Database connection established.")

                query = "SELECT user_id, password FROM user WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                print(f"Database query executed. User: {user}")

                if user:
                    user_id, hashed_password = user
                    print(f"User found. User ID: {user_id}, Hashed Password: [PROTECTED]")

                    if verify_password(hashed_password, password):
                        print("Password verified successfully.")
                        session['user_id'] = user_id
                        session['email'] = email
                        print(f"Session after login: {session}")
                        flash('Login successful!', 'success')
                        
                        return redirect_to('user_dashboard.user_dashboard')
                    else:
                        login_error = 'Invalid email or password.'
                        print("Invalid password.")
                else:
                    login_error = 'User not found.'
                    print("User not found.")

                cursor.close()
                close_db_connection(connection)
                print("Database connection closed.")

            except Exception as e:
                print(f"Exception occurred: {e}")
                flash(f"An unexpected error occurred: {e}", 'danger')

    response = make_response(render_template('login/user_login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error))
    response = disable_caching(response)
    return response
