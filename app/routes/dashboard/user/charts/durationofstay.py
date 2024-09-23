from app.models.database import get_cursor, close_db_connection

def get_vehicle_stay_durations(user_id):
    cursor, connection = get_cursor()

    cursor.execute('''
        SELECT 
            DATE_FORMAT(time_logs.time_in, '%Y-%m-%d %H:00:00') AS hour,
            AVG(TIMESTAMPDIFF(HOUR, time_logs.time_in, time_logs.time_out)) AS avg_stay_duration
        FROM time_logs
        INNER JOIN vehicle ON time_logs.vehicle_id = vehicle.vehicle_id
        WHERE time_logs.time_out IS NOT NULL
          AND time_logs.time_in >= CURDATE() - INTERVAL 7 DAY
          AND vehicle.user_id = %s
        GROUP BY hour
        ORDER BY hour ASC;
    ''', (user_id,))
    stay_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Stay Data:", stay_data)

    cursor.close()
    close_db_connection(connection)

    labels = [row[0] for row in stay_data] 
    durations = [row[1] for row in stay_data]  

    print("Labels:", labels)
    print("Durations:", durations)

    return {
        'labels': labels,
        'duration': durations
    }
