from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from ..utils.forms import BaseLoginForm  # Import the new base form
from app.models.database import get_cursor, close_db_connection
from ..utils.utils import verify_password, verify_recaptcha

admin_login_bp = Blueprint('admin_login', __name__)

@admin_login_bp.route('', methods=['GET', 'POST'])
def admin_login():
    print(f"Session before login attempt: {session}") 

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
                
                query = "SELECT admin_id, password FROM admin WHERE email = %s"
                cursor.execute(query, (email,))
                admin = cursor.fetchone()
                print(f"Database query executed. Admin: {admin}") 

                if admin:
                    admin_id, hashed_password = admin
                    print(f"Admin found. Admin ID: {admin_id}, Hashed Password: [PROTECTED]") 
                    
                    if verify_password(hashed_password, password):
                        print("Password verified successfully.") 
                        session['admin_id'] = admin_id
                        session['email'] = email
                        print(f"Session after login: {session}") 
                        flash('Login successful!', 'success')
                        return redirect(url_for('admin_dashboard.admin_dashboard'))
                    else:
                        login_error = 'Invalid email or password.'
                        print("Invalid email or password.")
                        flash('Invalid email or password.', 'danger')
                else:
                    login_error = 'Admin not found.'
                    print("Admin not found.")  
                    flash('Invalid email or password.', 'danger')
                
                cursor.close()
                close_db_connection(connection)
                print("Database connection closed.")  
            
            except Exception as e:
                print(f"Exception occurred: {e}") 
                flash(f"An unexpected error occurred: {e}", 'danger')
                cursor.close()
                close_db_connection(connection)

    return render_template('login/admin_login.html', form=form, recaptcha_error=recaptcha_error, login_error=login_error)
