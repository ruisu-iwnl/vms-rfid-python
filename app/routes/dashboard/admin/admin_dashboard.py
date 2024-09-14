from flask import Blueprint, render_template,session
from app.routes.utils.session import check_session

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('')
def admin_dashboard():

    response = check_session('admin')
    
    if response:
        return response
    
    print(f"Session active in admin_dashboard: {session}")
    return render_template('dashboard/admin/admin_dashboard.html')
