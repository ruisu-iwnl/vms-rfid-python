from app.models.database import get_cursor, close_db_connection

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
