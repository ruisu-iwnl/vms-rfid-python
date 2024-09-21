

from app.models.database import get_cursor, close_db_connection

def get_time_in_time_out_comparison(user_id):
    cursor, connection = get_cursor()

    cursor.execute('''
        SELECT DATE(time_in) AS date, COUNT(*) AS time_in_count
        FROM time_logs
        WHERE time_in >= CURDATE() - INTERVAL 7 DAY AND vehicle_id IN (
            SELECT vehicle_id FROM vehicle WHERE user_id = %s
        )
        GROUP BY DATE(time_in)
        ORDER BY DATE(time_in);
    ''', (user_id,))
    time_in_data = cursor.fetchall()

    cursor.execute('''
        SELECT DATE(time_out) AS date, COUNT(*) AS time_out_count
        FROM time_logs
        WHERE time_out >= CURDATE() - INTERVAL 7 DAY AND vehicle_id IN (
            SELECT vehicle_id FROM vehicle WHERE user_id = %s
        )
        GROUP BY DATE(time_out)
        ORDER BY DATE(time_out);
    ''', (user_id,))
    time_out_data = cursor.fetchall()

    print("SQL Query Executed for Time-Ins")
    print("Raw Time-In Data:", time_in_data)
    print("SQL Query Executed for Time-Outs")
    print("Raw Time-Out Data:", time_out_data)

    cursor.close()
    close_db_connection(connection)

    dates = sorted(set(row[0] for row in time_in_data) | set(row[0] for row in time_out_data))
    time_in_counts = [next((count for date, count in time_in_data if date == d), 0) for d in dates]
    time_out_counts = [next((count for date, count in time_out_data if date == d), 0) for d in dates]

    print("Dates:", dates)
    print("Time-In Counts:", time_in_counts)
    print("Time-Out Counts:", time_out_counts)

    return {
        'labels': [date.strftime('%Y-%m-%d') for date in dates],
        'timein': time_in_counts,
        'timeout': time_out_counts
    }
