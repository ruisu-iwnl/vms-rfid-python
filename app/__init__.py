from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os
from .routes.main import main_bp

#login and register routes
from .routes.login.admin_login import admin_login_bp
from .routes.login.user_login import user_login_bp
from .routes.register.admin_register import admin_register_bp
from .routes.register.user_register import user_register_bp
# admin dashboard routes
from .routes.dashboard.admin.admin_dashboard import admin_dashboard_bp  
from .routes.dashboard.admin.timeinout import timeinout_bp
from .routes.dashboard.admin.userlist import userlist_bp
from .routes.dashboard.admin.activitylog import activitylog_bp
# user dashboard routes
from .routes.dashboard.user.user_dashboard import user_dashboard_bp
from .routes.dashboard.user.vehicles import vehicles_bp


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)  

    CSRFProtect(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_login_bp, url_prefix='/login/admin')
    app.register_blueprint(user_login_bp, url_prefix='/login/user')
    app.register_blueprint(admin_register_bp, url_prefix='/register/admin')
    app.register_blueprint(user_register_bp, url_prefix='/register/user')
    #user dashboard
    app.register_blueprint(user_dashboard_bp, url_prefix='/dashboard/guide')
    app.register_blueprint(vehicles_bp, url_prefix='/dashboard/vehicles')
    #admin dashboard
    app.register_blueprint(admin_dashboard_bp, url_prefix='/dashboard/admin')  
    app.register_blueprint(timeinout_bp, url_prefix='/dashboard/timeinout')
    app.register_blueprint(userlist_bp, url_prefix='/dashboard/userlist')
    app.register_blueprint(activitylog_bp, url_prefix='/dashboard/activitylog')



    return app

