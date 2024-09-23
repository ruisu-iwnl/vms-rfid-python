from app.models.database import get_cursor, close_db_connection

def get_vehicle_stay_durations():
    cursor, connection = get_cursor()

    # Get average vehicle stay durations for each hour of the day over the last 7 days
    cursor.execute('''
        SELECT 
            DATE_FORMAT(time_logs.time_in, '%Y-%m-%d %H:00:00') AS hour,
            AVG(TIMESTAMPDIFF(HOUR, time_logs.time_in, time_logs.time_out)) AS avg_stay_duration
        FROM time_logs
        WHERE time_logs.time_out IS NOT NULL
          AND time_logs.time_in >= CURDATE() - INTERVAL 7 DAY
        GROUP BY hour
        ORDER BY hour ASC;
    ''')
    stay_data = cursor.fetchall()

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
