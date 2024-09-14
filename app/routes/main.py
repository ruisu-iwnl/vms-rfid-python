from flask import Blueprint, render_template
from app.routes.utils.utils import logout

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/logout', methods=['POST'])
def logout_view():
    return logout()