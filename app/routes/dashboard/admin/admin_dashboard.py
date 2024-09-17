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

def get_daily_vehicle_distribution():
    cursor, connection = get_cursor()

    # Get daily vehicle distribution for the last 7 days based on vehicle creation dates
    cursor.execute('''
        SELECT DATE(created_at) AS date, COUNT(vehicle_id) AS vehicle_count
        FROM vehicle
        WHERE created_at >= CURDATE() - INTERVAL 6 DAY
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at);
    ''')
    daily_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Data:", daily_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    labels = [row[0].strftime('%Y-%m-%d') for row in daily_data]
    data = [row[1] for row in daily_data]

    # Debugging output
    print("Labels:", labels)
    print("Data:", data)

    return {
        'labels': labels,
        'data': data
    }



@admin_dashboard_bp.route('')
def admin_dashboard():
    response = check_access('admin')
    
    if response:
        return response

    dashboard_data = get_dashboard_data()
    daily_data = get_daily_vehicle_distribution()

    print(f"Session active in admin_dashboard: {session}")
    return render_template(
        'dashboard/admin/admin_dashboard.html',
        **dashboard_data,
        daily_data=daily_data
    )
