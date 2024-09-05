from flask import Flask
from .routes.main import main_bp
from .routes.login.admin_login import admin_login_bp
from .routes.login.user_login import user_login_bp
from .routes.register.admin_register import admin_register_bp
from .routes.register.user_register import user_register_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_login_bp, url_prefix='/login/admin')
    app.register_blueprint(user_login_bp, url_prefix='/login/user')
    app.register_blueprint(admin_register_bp, url_prefix='/register/admin')
    app.register_blueprint(user_register_bp, url_prefix='/register/user')

    return app
