from app.models.database import get_cursor, close_db_connection

def get_vehicle_stay_durations(user_id):
    cursor, connection = get_cursor()

    # Get vehicle stay durations for the last 7 days based on time_in and time_out for the logged-in user's vehicles
    cursor.execute('''
        SELECT vehicle.licenseplate, TIMESTAMPDIFF(HOUR, time_logs.time_in, time_logs.time_out) AS stay_duration
        FROM time_logs
        INNER JOIN vehicle ON time_logs.vehicle_id = vehicle.vehicle_id
        WHERE time_logs.time_out IS NOT NULL
          AND time_logs.time_in >= CURDATE() - INTERVAL 7 DAY
          AND vehicle.user_id = %s
        ORDER BY time_logs.time_in DESC;
    ''', (user_id,))
    stay_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Stay Data:", stay_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    labels = [row[0] for row in stay_data]  # Vehicle license plates
    durations = [row[1] for row in stay_data]  # Duration of stay in hours

    # Debugging output
    print("Labels:", labels)
    print("Durations:", durations)

    return {
        'labels': labels,
        'duration': durations
    }
