from app.models.database import get_cursor, close_db_connection
from datetime import datetime, timedelta

def most_active_days():
    cursor, connection = get_cursor()

    # Get vehicle entry data for the last 7 days
    cursor.execute('''
        SELECT DATE_FORMAT(time_in, '%W') AS day_of_week, COUNT(vehicle_id) AS vehicle_count
        FROM time_logs
        WHERE DATE(time_in) >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
        GROUP BY day_of_week
        ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    ''')
    weekly_data = cursor.fetchall()

    cursor.close()
    close_db_connection(connection)

    # Define all days of the week
    all_days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    vehicle_count_by_day = {day: 0 for day in all_days_of_week}

    # Update the data with the fetched results
    for row in weekly_data:
        day_of_week = row[0]
        vehicle_count = row[1]
        vehicle_count_by_day[day_of_week] = vehicle_count

    labels = all_days_of_week
    data = [vehicle_count_by_day[day] for day in all_days_of_week]

    return {
        'labels': labels,
        'data': data
    }
