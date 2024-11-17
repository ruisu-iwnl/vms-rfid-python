from flask import Blueprint, render_template, session
from app.routes.utils.session import check_access
from app.routes.dashboard.user.charts.timeinoutcompare import get_time_in_time_out_comparison
from app.routes.dashboard.user.charts.peakhours import get_peak_hours_of_vehicle_entries
from app.routes.dashboard.user.charts.durationofstay import get_vehicle_stay_durations
from app.routes.dashboard.user.charts.mostactivedays import most_active_days
from app.routes.utils.utils import get_name, get_emp_profile_info

user_dashboard_bp = Blueprint('user_dashboard', __name__)

@user_dashboard_bp.route('')
def user_dashboard():
    response = check_access('user')
    if response:
        return response

    user_id = session['user_id']
    user_name = get_name(user_id)

    time_in_time_out_data = get_time_in_time_out_comparison(user_id)
    peak_hours_data = get_peak_hours_of_vehicle_entries()
    vehicle_stay_durations_data = get_vehicle_stay_durations(user_id)
    most_active_days_data = most_active_days(user_id)

    user_profile = get_emp_profile_info(user_id)

    return render_template('dashboard/user/user_dashboard.html',
                            user_name=user_name,
                            time_in_time_out_data=time_in_time_out_data,
                            peak_hours_data=peak_hours_data,
                            vehicle_stay_durations_data=vehicle_stay_durations_data,
                            most_active_days_data=most_active_days_data,
                            user=user_profile)
