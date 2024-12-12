import os
from flask_mail import Mail, Message
mail = Mail()

def send_approved_notification(recipient):
    try:
        print("Attempting to connect to the SMTP server...")
        with mail.connect() as conn:
            print(f"Connected to SMTP server: {os.getenv('SMTP_SERVER')}:{os.getenv('SMTP_PORT')}")
            msg = Message(
                subject='Account Approved - Welcome to TimeGuard!',
                sender=os.getenv('SMTP_USERNAME'),
                recipients=[recipient],
                body=("Congratulations! Your account has been approved. You can now log in to the system using the email and password you registered with. "
                      "If you encounter any issues, please contact support.")
            )
            print(f"Sending email to {recipient}")
            conn.send(msg)
            print("Approval notification sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

def send_deny_notification(recipient):
    try:
        print("Attempting to connect to the SMTP server...")
        with mail.connect() as conn:
            print(f"Connected to SMTP server: {os.getenv('SMTP_SERVER')}:{os.getenv('SMTP_PORT')}")
            msg = Message(
                subject='Account Denied - Contact Support',
                sender=os.getenv('SMTP_USERNAME'),
                recipients=[recipient],
                body=("Unfortunately, your account could not be approved at this time. The reason may include one or more of the following: \n"
                      "- Incorrect or invalid documents \n"
                      "- Missing required information \n"
                      "- Discrepancies found in your submitted details\n\n"
                      "If you have any questions or need further assistance, please contact support.")
            )
            print(f"Sending email to {recipient}")
            conn.send(msg)
            print("Denial notification sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
