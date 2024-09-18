from app.models.database import get_cursor, close_db_connection
from datetime import datetime

def log_login_activity(user_id, account_type, action):
    """
    Logs the login activity into the appropriate activity log table.
    """
    cursor, connection = get_cursor()
    activity_timestamp = datetime.now()
    details = f"{action} - User ID: {user_id}"

    if account_type == 'Admin':
        query = """
            INSERT INTO admin_activity_log (admin_id, activity_type, activity_timestamp, details)
            VALUES (%s, %s, %s, %s);
        """
    elif account_type == 'User':
        query = """
            INSERT INTO user_activity_log (user_id, activity_type, activity_timestamp, details)
            VALUES (%s, %s, %s, %s);
        """
    else:
        print("Invalid account type.")
        return

    try:
        cursor.execute(query, (user_id, action, activity_timestamp, details))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error logging activity: {e}")
    finally:
        close_db_connection(connection)
