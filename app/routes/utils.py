from werkzeug.security import generate_password_hash

def hash_password(password):
    """
    Hashes the given password using Werkzeug's generate_password_hash function.
    """
    hashed_password = generate_password_hash(password)
    return hashed_password