from flask import Blueprint, render_template,session

user_dashboard_bp = Blueprint('user_dashboard', __name__)

@user_dashboard_bp.route('')
def user_dashboard():
    print(f"Session active in admin_dashboard: {session}")
    return render_template('dashboard/user/user_dashboard.html')
