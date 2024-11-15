from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os
from .routes.main import main_bp

#login
from .routes.login.login import login_bp
# Registration routes
from .routes.register.admin_register import admin_register_bp
from .routes.register.user_register import user_register_bp
# Admin dashboard routes
from .routes.dashboard.admin.admin_dashboard import admin_dashboard_bp  
from .routes.dashboard.admin.timeinout import timeinout_bp
from .routes.dashboard.admin.userlist import userlist_bp
from .routes.dashboard.admin.activitylog import activitylog_bp
from .routes.dashboard.admin.rfid import rfid_bp
# from .routes.dashboard.admin.survey_admin import survey_admin_bp
# User dashboard routes
from .routes.dashboard.user.user_dashboard import user_dashboard_bp
from .routes.dashboard.user.vehicles import vehicles_bp
# from .routes.dashboard.user.survey_user import survey_user_bp

from .routes.error import error_bp

from .routes.dashboard.user.modals.addvehicle import add_vehicle_bp
from .routes.dashboard.admin.modals.adduser import adduser_bp
from .routes.dashboard.admin.modals.addvehicle import user_vehicle_bp

from .routes.dashboard.admin.manageadmin import adminlist_bp
from .routes.dashboard.admin.modals.addadmin import addadmin_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)  

    CSRFProtect(app)

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
    # app.register_blueprint(survey_admin_bp, url_prefix='/survey/admin')
    # app.register_blueprint(survey_user_bp, url_prefix='/survey/user')

    app.register_blueprint(add_vehicle_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(adduser_bp)
    app.register_blueprint(user_vehicle_bp)

    app.register_blueprint(adminlist_bp, url_prefix='/adminlist')
    app.register_blueprint(addadmin_bp)

    return app
