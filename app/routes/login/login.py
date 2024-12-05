import os
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from ..utils.forms import BaseLoginForm
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import verify_password, verify_recaptcha
from ..utils.session import check_logged_in_redirect
from ..utils.cache import disable_caching, redirect_to
from ..utils.activity_log import log_login_activity

login_bp = Blueprint('login', __name__)

@login_bp.route('', methods=['GET', 'POST'])
def login():
    """
    Handles both Admin and User login without blocking unverified users.
    """
    response = check_logged_in_redirect()
    if response:
        return response

    form = BaseLoginForm()
    recaptcha_error = None
    login_error = None

    disable_recaptcha = os.getenv('DISABLE_RECAPTCHA', 'False').lower() == 'true'

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        recaptcha_response = request.form.get('g-recaptcha-response')

        if not disable_recaptcha and not verify_recaptcha(recaptcha_response):
            recaptcha_error = 'reCAPTCHA verification failed. Please try again.'
        else:
            try:
                cursor, connection = get_cursor()

                # Check if user is an admin
                cursor.execute("SELECT email, is_super_admin, deleted_at FROM admin WHERE email = %s", (email,))
                admin = cursor.fetchone()
                
                if admin:
                    user_type = 'admin'
                    table_name = 'admin'
                    user_id_column = 'admin_id'
                    is_super_admin = admin[1]
                    deleted_at = admin[2]
                    
                    if deleted_at:
                        login_error = 'Your account has been removed. Please contact support.'
                        flash(login_error, 'danger')
                        log_login_activity(None, 'Admin', 'Login failed: Account soft-deleted')
                        return render_template('login/login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error)
                else:
                    # Check if user is a regular user
                    cursor.execute("SELECT email, deleted_at FROM user WHERE email = %s", (email,))
                    user = cursor.fetchone()
                    
                    if user:
                        user_type = 'user'
                        table_name = 'user'
                        user_id_column = 'user_id'
                        deleted_at = user[1]
                    else:
                        login_error = 'Invalid email or password.'
                        flash(login_error, 'danger')
                        log_login_activity(None, 'User', 'Login failed: User not found') 
                        return render_template('login/login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error)

                    if deleted_at:
                        login_error = 'Your account has been removed. Please contact support.'
                        flash(login_error, 'danger')
                        log_login_activity(None, 'User', 'Login failed: Account soft-deleted') 
                        return render_template('login/login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error)

                # Fetch user ID and password ID
                query = f"SELECT {user_id_column}, password_id FROM {table_name} WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user:
                    user_id, password_id = user

                    # Verify password
                    cursor.execute("SELECT password_hash FROM passwords WHERE password_id = %s", (password_id,))
                    password_record = cursor.fetchone()

                    if password_record:
                        hashed_password = password_record[0]

                        if verify_password(hashed_password, password):
                            session[f'{user_type}_id'] = user_id
                            session['email'] = email

                            if user_type == 'admin':
                                session['is_super_admin'] = is_super_admin

                            flash('Login successful!', 'success')
                            log_login_activity(user_id, user_type.capitalize(), 'Login successful')

                            dashboard_route = f'{user_type}_dashboard.{user_type}_dashboard'
                            return redirect_to(dashboard_route)
                        else:
                            login_error = 'Invalid email or password.'
                            flash('Invalid email or password.', 'danger')
                            log_login_activity(None, user_type.capitalize(), 'Login failed: Invalid password')
                    else:
                        login_error = 'Password not found.'
                        flash('An error occurred. Please try again later.', 'danger')
                else:
                    login_error = f'{user_type.capitalize()} not found.'
                    flash('Invalid email or password.', 'danger')
                    log_login_activity(None, user_type.capitalize(), 'Login failed: User not found')

            except Exception as e:
                flash(f"An unexpected error occurred: {e}", 'danger')
            finally:
                cursor.close()
                close_db_connection(connection)

    return render_template('login/login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error)
