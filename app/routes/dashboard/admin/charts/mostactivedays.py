from app.models.database import get_cursor, close_db_connection

def most_active_days():
    cursor, connection = get_cursor()

    # Get the number of vehicle entries for each day of the week
    cursor.execute('''
        SELECT DAYNAME(time_in) AS day_of_week, COUNT(vehicle_id) AS vehicle_count
        FROM time_logs
        WHERE DATE(time_in) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
        GROUP BY day_of_week
        ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    ''')
    weekly_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed")
    print("Raw Data:", weekly_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    labels = [row[0] for row in weekly_data]
    data = [row[1] for row in weekly_data]

    # Debugging output
    print("Labels:", labels)
    print("Data:", data)

    return {
        'labels': labels,
        'data': data
    }


