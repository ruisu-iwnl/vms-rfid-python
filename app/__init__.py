from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

from .routes.main import main_bp
from .routes.login.login import login_bp
from .routes.register.admin_register import admin_register_bp
from .routes.register.user_register import user_register_bp
from .routes.dashboard.admin.admin_dashboard import admin_dashboard_bp  
from .routes.dashboard.admin.timeinout import timeinout_bp
from .routes.dashboard.admin.userlist import userlist_bp
from .routes.dashboard.admin.activitylog import activitylog_bp
from .routes.dashboard.admin.rfid import rfid_bp
from .routes.dashboard.user.user_dashboard import user_dashboard_bp
from .routes.dashboard.user.vehicles import vehicles_bp
from .routes.error import error_bp
from .routes.dashboard.user.modals.addvehicle import add_vehicle_bp
from .routes.dashboard.admin.modals.adduser import adduser_bp
from .routes.dashboard.admin.modals.addvehicle import user_vehicle_bp
from .routes.dashboard.admin.manageadmin import adminlist_bp
from .routes.dashboard.admin.modals.addadmin import addadmin_bp
from .routes.termsandconditions import tc_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)  

    CSRFProtect(app)

    # Load environment variables from .env file
    load_dotenv()

    # Load SMTP configuration
    app.config.update(
        MAIL_SERVER=os.getenv('SMTP_SERVER'),
        MAIL_PORT=int(os.getenv('SMTP_PORT')),
        MAIL_USE_TLS=bool(os.getenv('SMTP_USE_TLS')),
        MAIL_USERNAME=os.getenv('SMTP_USERNAME'),
        MAIL_PASSWORD=os.getenv('SMTP_PASSWORD')
    )

    mail = Mail(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(admin_register_bp, url_prefix='/register/admin')
    app.register_blueprint(user_register_bp, url_prefix='/register/user')
    # User dashboard
    app.register_blueprint(user_dashboard_bp, url_prefix='/dashboard/user')
    app.register_blueprint(vehicles_bp, url_prefix='/dashboard/vehicles')
    # Admin dashboard
    app.register_blueprint(admin_dashboard_bp, url_prefix='/dashboard/admin')  
    app.register_blueprint(timeinout_bp, url_prefix='/dashboard/timeinout')
    app.register_blueprint(userlist_bp, url_prefix='/dashboard/userlist')
    app.register_blueprint(activitylog_bp, url_prefix='/dashboard/activitylog')
    app.register_blueprint(rfid_bp, url_prefix='/dashboard/rfid')
    app.register_blueprint(add_vehicle_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(adduser_bp)
    app.register_blueprint(user_vehicle_bp)

    app.register_blueprint(adminlist_bp, url_prefix='/adminlist')
    app.register_blueprint(addadmin_bp)

    app.register_blueprint(tc_bp)

    # Configuration for test email sending
    app.config['SEND_TEST_EMAIL'] = os.getenv('SEND_TEST_EMAIL', 'false').lower() in ['true', '1', 't']

    @app.route('/send-email')
    def send_email():
        if not app.config['SEND_TEST_EMAIL']:
            return "Test email sending is disabled."

        try:
            print("Attempting to connect to the SMTP server...")
            with mail.connect() as conn:
                print(f"Connected to SMTP server: {os.getenv('SMTP_SERVER')}:{os.getenv('SMTP_PORT')}")
                msg = Message(
                    subject='Subject',
                    sender=os.getenv('SMTP_USERNAME'),
                    recipients=[os.getenv('SMTP_RECIPIENT')],
                    body="This is a test email."
                )
                print(f"Sending email to {os.getenv('SMTP_RECIPIENT')}")
                conn.send(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Error: {e}"

        return "Email sent!"

    return app
