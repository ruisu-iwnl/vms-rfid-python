from app.models.database import get_cursor, close_db_connection

def get_peak_hours_of_vehicle_entries():
    cursor, connection = get_cursor()

    # Get hourly vehicle entry data for the current day based on time logs
    cursor.execute('''
        SELECT DATE_FORMAT(time_in, '%H:00 - %H:59') AS hour, COUNT(vehicle_id) AS vehicle_count
        FROM time_logs
        WHERE DATE(time_in) = CURDATE()
        GROUP BY hour
        ORDER BY hour;
    ''')
    hourly_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Data:", hourly_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    labels = [row[0] for row in hourly_data]
    data = [row[1] for row in hourly_data]

    # Debugging output
    print("Labels:", labels)
    print("Data:", data)

    return {
        'labels': labels,
        'data': data
    }
