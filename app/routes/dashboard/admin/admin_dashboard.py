from flask import Blueprint, render_template, session
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection
from app.routes.dashboard.admin.charts.vehicledistribution import get_daily_vehicle_distribution
from app.routes.dashboard.admin.charts.timeinout_comparison import get_time_in_time_out_comparison
from app.routes.dashboard.admin.charts.basic_dashboarddata import get_dashboard_data
from app.routes.dashboard.admin.charts.durationofstay import get_vehicle_stay_durations

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('')
def admin_dashboard():
    response = check_access('admin')
    
    if response:
        return response

    dashboard_data = get_dashboard_data()
    daily_data = get_daily_vehicle_distribution()
    time_in_time_out_data = get_time_in_time_out_comparison()
    vehicle_stay_durations_data = get_vehicle_stay_durations()
    
    print(f"Session active in admin_dashboard: {session}")
    print("Daily Data:", daily_data)
    print("Time-In/Time-Out Data:", time_in_time_out_data)
    
    return render_template(
        'dashboard/admin/admin_dashboard.html',
        **dashboard_data,
        daily_data=daily_data,
        time_in_time_out_data=time_in_time_out_data,
        vehicle_stay_durations_data=vehicle_stay_durations_data
    )