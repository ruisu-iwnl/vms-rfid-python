from flask import Blueprint, render_template

user_dashboard_bp = Blueprint('user_dashboard', __name__)

@user_dashboard_bp.route('')
def admin_dashboard():
    return render_template('dashboard/user/user_dashboard.html')
