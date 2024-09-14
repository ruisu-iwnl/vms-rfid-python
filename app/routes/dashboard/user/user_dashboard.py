from flask import Blueprint, render_template,session
from app.routes.utils.session import check_access

user_dashboard_bp = Blueprint('user_dashboard', __name__)

@user_dashboard_bp.route('')
def user_dashboard():

    response = check_access('user')
    if response:
        return response

    print(f"Session active in user_dashboard: {session}")
    return render_template('dashboard/user/user_dashboard.html')
