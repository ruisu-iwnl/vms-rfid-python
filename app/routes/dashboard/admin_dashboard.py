from flask import Blueprint, render_template

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('')
def admin_dashboard():
    return render_template('dashboard/admin/admin_dashboard.html')
