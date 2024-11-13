from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import requests
from flask import session,redirect,url_for
from app.models.database import get_cursor, close_db_connection

load_dotenv()

def get_user_profile_info(user_id):
    cursor, connection = get_cursor()
    try:
        cursor.execute("""
            SELECT emp_no, firstname, lastname, email, contactnumber, profile_image
            FROM user
            WHERE user_id = %s
        """, (user_id,))
        user_profile = cursor.fetchone()

        if user_profile:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM vehicle 
                WHERE user_id = %s
            """, (user_id,))
            vehicle_count = cursor.fetchone()[0]

            return {
                'emp_no': user_profile[0],
                'firstname': user_profile[1],
                'lastname': user_profile[2],
                'email': user_profile[3],
                'contactnumber': user_profile[4],
                'profile_image': user_profile[5],
                'vehicle_count': vehicle_count
            }
        else:
            return None  

    finally:
        close_db_connection(connection)


def get_name(user_id):
    cursor, connection = get_cursor()
    try:
        query = "SELECT firstname FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    finally:
        cursor.close()
        close_db_connection(connection)

def logout():
    """
    Logs out the current user by clearing the session.
    """
    session.clear()
    print("User logged out. Session cleared.")
    return redirect(url_for('main.index'))

def verify_password(stored_password_hash, provided_password):
    """
    Verifies if the provided password matches the stored hashed password.
    
    Args:
        stored_password_hash (str): The hashed password stored in the database.
        provided_password (str): The password provided by the user trying to log in.
    
    Returns:
        bool: True if passwords match, False otherwise.
    """
    return check_password_hash(stored_password_hash, provided_password)

def hash_password(password):
    """
    Hashes the given password using Werkzeug's generate_password_hash function.
    """
    hashed_password = generate_password_hash(password)
    return hashed_password

def verify_recaptcha(recaptcha_response):
    secret_key = os.getenv('RECAPTCHA_SECRET_KEY')
    
    if not secret_key:
        raise ValueError("RECAPTCHA_SECRET_KEY is not set in the environment variables.")
    
    payload = {'secret': secret_key, 'response': recaptcha_response}
    
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    
    if response.status_code != 200:
        print(f"reCAPTCHA API request failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return False
    
    result = response.json()
    
    return result.get('success')

def check_existing_registration(email):
    """
    Checks if the email is already registered as a user or admin.
    Returns a tuple (is_registered_as_user, is_registered_as_admin).
    """
    cursor, connection = get_cursor()
    try:
        cursor.execute("SELECT 1 FROM user WHERE email = %s LIMIT 1", (email,))
        is_registered_as_user = cursor.fetchone() is not None

        cursor.execute("SELECT 1 FROM admin WHERE email = %s LIMIT 1", (email,))
        is_registered_as_admin = cursor.fetchone() is not None

        return is_registered_as_user, is_registered_as_admin
    finally:
        cursor.close()
        close_db_connection(connection)

