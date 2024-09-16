from flask import Blueprint, render_template, session
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

def get_dashboard_data():
    cursor, connection = get_cursor()

    # Get total number of users
    cursor.execute('SELECT COUNT(*) FROM user')
    total_users = cursor.fetchone()[0]
    
    # Get total number of vehicles
    cursor.execute('SELECT COUNT(*) FROM vehicle')
    total_vehicles = cursor.fetchone()[0]
    
    # Get average number of vehicles per user
    cursor.execute('''
        SELECT AVG(vehicle_count) 
        FROM (
            SELECT COUNT(*) AS vehicle_count
            FROM vehicle
            GROUP BY user_id
        ) AS subquery
    ''')
    avg_vehicles_per_user = cursor.fetchone()[0] or 0
    avg_vehicles_per_user = round(avg_vehicles_per_user, 2)
    
    # Get number of users with no vehicles
    cursor.execute('''
        SELECT COUNT(*) 
        FROM user u
        LEFT JOIN vehicle v ON u.user_id = v.user_id
        WHERE v.vehicle_id IS NULL
    ''')
    users_with_no_vehicles = cursor.fetchone()[0]
    
    # Get total number of RFID tags
    cursor.execute('SELECT COUNT(*) FROM rfid')
    total_rfid_tags = cursor.fetchone()[0]

    # Get active RFID tags count (assuming active means not null in time_logs)
    cursor.execute('''
        SELECT COUNT(DISTINCT r.rfid_id)
        FROM rfid r
        LEFT JOIN time_logs t ON r.rfid_id = t.rfid_id
        WHERE t.time_out IS NULL
    ''')
    active_rfid_count = cursor.fetchone()[0]

    # Get recent user registrations (last 30 days)
    cursor.execute('''
        SELECT COUNT(*) 
        FROM user 
        WHERE created_at >= NOW() - INTERVAL 30 DAY
    ''')
    recent_user_registrations = cursor.fetchone()[0]

    # Get most common vehicle model
    cursor.execute('''
        SELECT model
        FROM vehicle
        GROUP BY model
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ''')
    most_common_vehicle_model = cursor.fetchone()[0]

    cursor.close()
    close_db_connection(connection)

    return {
        'total_users': total_users,
        'total_vehicles': total_vehicles,
        'avg_vehicles_per_user': avg_vehicles_per_user,
        'users_with_no_vehicles': users_with_no_vehicles,
        'total_rfid_tags': total_rfid_tags,
        'active_rfid_count': active_rfid_count,
        'recent_user_registrations': recent_user_registrations,
        'most_common_vehicle_model': most_common_vehicle_model
    }


@admin_dashboard_bp.route('')
def admin_dashboard():
    response = check_access('admin')
    
    if response:
        return response

    dashboard_data = get_dashboard_data()

    print(f"Session active in admin_dashboard: {session}")

    return render_template(
        'dashboard/admin/admin_dashboard.html',
        **dashboard_data
    )
