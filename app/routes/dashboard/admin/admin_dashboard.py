from flask import Blueprint, render_template, session
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection
from app.routes.dashboard.admin.charts.vehicledistribution import get_daily_vehicle_distribution
from app.routes.dashboard.admin.charts.timeinout_comparison import get_time_in_time_out_comparison
from app.routes.dashboard.admin.charts.basic_dashboarddata import get_dashboard_data
from app.routes.dashboard.admin.charts.durationofstay import get_vehicle_stay_durations
from app.routes.dashboard.admin.charts.user_registered_weekly import get_daily_user_registration
from app.routes.dashboard.admin.charts.mostactivedays import most_active_days
from app.routes.dashboard.admin.charts.peakhours import get_peak_hours_of_vehicle_entries

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('')
def admin_dashboard():
    response = check_access('admin')
    
    if response:
        return response

    is_super_admin = session.get('is_super_admin', False)

    # Get dashboard data
    dashboard_data = get_dashboard_data()
    daily_data = get_daily_vehicle_distribution()
    time_in_time_out_data = get_time_in_time_out_comparison()
    vehicle_stay_durations_data = get_vehicle_stay_durations()
    user_registration_data = get_daily_user_registration()
    most_active_days_data = most_active_days()
    peak_hours_data = get_peak_hours_of_vehicle_entries()

    # Print session for debugging purposes
    # print(f"Session active in admin_dashboard: {session}")
    # print("Daily Data:", daily_data)
    # # print("duration of stay data:", vehicle_stay_durations_data)
    # print("Time-In/Time-Out Data:", time_in_time_out_data)
    # print("User Register Data:", user_registration_data)
    # print("Most Active Days Entry:", most_active_days_data)
    # print("Peak Hours:", peak_hours_data)

    if is_super_admin:
        print("This admin is a super admin.")

        super_admin_features = True
    else:
        print("This admin is NOT a super admin.")
        super_admin_features = False

    return render_template(
        'dashboard/admin/admin_dashboard.html',
        **dashboard_data,
        daily_data=daily_data,
        time_in_time_out_data=time_in_time_out_data,
        vehicle_stay_durations_data=vehicle_stay_durations_data,
        user_registration_data=user_registration_data,
        most_active_days_data=most_active_days_data,
        peak_hours_data=peak_hours_data,
        super_admin_features=super_admin_features  
    )
