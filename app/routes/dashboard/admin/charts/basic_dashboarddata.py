from app.models.database import get_cursor, close_db_connection

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

    # Get total RFID tags registered to a vehicle
    cursor.execute('''
        SELECT COUNT(*)
        FROM rfid
        WHERE vehicle_id IS NOT NULL
    ''')
    registered_rfid_count = cursor.fetchone()[0]


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
        'registered_rfid_count': registered_rfid_count,
        'recent_user_registrations': recent_user_registrations,
        'most_common_vehicle_model': most_common_vehicle_model
    }

