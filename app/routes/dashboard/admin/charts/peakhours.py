from app.models.database import get_cursor, close_db_connection
from datetime import datetime

def get_peak_hours_of_vehicle_entries():
    cursor, connection = get_cursor()

    # Get hourly vehicle entry data for the current day
    cursor.execute('''
        SELECT DATE_FORMAT(time_in, '%H') AS hour, COUNT(vehicle_id) AS vehicle_count
        FROM time_logs
        WHERE DATE(time_in) = CURDATE()
        GROUP BY hour
        ORDER BY hour;
    ''')
    hourly_data = cursor.fetchall()

    cursor.close()
    close_db_connection(connection)

    all_hours = [f"{str(i).zfill(2)}:00 - {str(i).zfill(2)}:59" for i in range(24)]
    vehicle_count_by_hour = {f"{str(i).zfill(2)}": 0 for i in range(24)}  

    for row in hourly_data:
        hour = row[0] 
        vehicle_count = row[1]
        vehicle_count_by_hour[hour] = vehicle_count


    labels = all_hours
    data = [vehicle_count_by_hour[hour] for hour in vehicle_count_by_hour]

    return {
        'labels': labels,
        'data': data
    }
