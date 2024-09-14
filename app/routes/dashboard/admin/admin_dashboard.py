from flask import Blueprint, render_template,session

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('')
def admin_dashboard():
    print(f"Session active in admin_dashboard: {session}")
    return render_template('dashboard/admin/admin_dashboard.html')
