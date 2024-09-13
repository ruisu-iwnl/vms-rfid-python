from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
import requests

load_dotenv()

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
