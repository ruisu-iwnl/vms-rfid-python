from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import requests
from flask import session,redirect,url_for
from app.models.database import get_cursor, close_db_connection

load_dotenv()

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

