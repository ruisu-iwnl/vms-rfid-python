from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash
from ..forms import UserLoginForm
from app.models.database import get_cursor, close_db_connection
from ..utils import verify_password

user_login_bp = Blueprint('user_login', __name__)

@user_login_bp.route('', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        print(f"Form submitted. Email: {email}, Password: [PROTECTED]")

        cursor, connection = get_cursor()
        print("Database connection established.")
        
        query = "SELECT user_id, password FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        print(f"Database query executed. User: {user}")
        
        if user:
            user_id, hashed_password = user
            print(f"User found. User ID: {user_id}, Hashed Password: {hashed_password}")
            
            if verify_password(hashed_password, password):
                print("Password verified successfully.")  
                session['user_id'] = user_id
                session['email'] = email
                flash('Login successful!', 'success')
                return redirect(url_for('user_dashboard.user_dashboard'))
            else:
                print("Invalid password.") 
                flash('Invalid email or password.', 'danger')
        else:
            print("User not found.")
            flash('Invalid email or password.', 'danger')
        
        close_db_connection(connection)
        print("Database connection closed.")
    
    return render_template('login/user_login.html', form=form)
