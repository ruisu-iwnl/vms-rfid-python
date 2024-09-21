from app.models.database import get_cursor, close_db_connection

def get_peak_hours_of_vehicle_entries(user_id):
    cursor, connection = get_cursor()

    # Get hourly vehicle entry data for the current day based on time logs for the logged-in user's vehicles
    cursor.execute('''
        SELECT DATE_FORMAT(time_in, '%H:00 - %H:59') AS hour, COUNT(vehicle_id) AS vehicle_count
        FROM time_logs
        WHERE DATE(time_in) = CURDATE() 
          AND vehicle_id IN (
              SELECT vehicle_id FROM vehicle WHERE user_id = %s
          )
        GROUP BY hour
        ORDER BY hour;
    ''', (user_id,))
    hourly_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Data:", hourly_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    labels = [row[0] for row in hourly_data]  # Hours of the day
    data = [row[1] for row in hourly_data]    # Vehicle counts

    # Debugging output
    print("Labels:", labels)
    print("Data:", data)

    return {
        'labels': labels,
        'data': data
    }
