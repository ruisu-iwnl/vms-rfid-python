from flask import Blueprint, render_template
from app.routes.utils.utils import logout
from app.routes.utils.session import check_logged_in_redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    response = check_logged_in_redirect()
    if response:
        return response
    return render_template('index.html')

@main_bp.route('/logout', methods=['POST'])
def logout_view():
    return logout()