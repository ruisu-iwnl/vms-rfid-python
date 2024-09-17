from app.models.database import get_cursor, close_db_connection

def get_time_in_time_out_comparison():
    cursor, connection = get_cursor()

    # Get the total number of time-ins and time-outs for the last 7 days
    cursor.execute('''
        SELECT DATE(time_in) AS date, COUNT(*) AS time_in_count
        FROM time_logs
        WHERE time_in >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE(time_in)
        ORDER BY DATE(time_in);
    ''')
    time_in_data = cursor.fetchall()

    cursor.execute('''
        SELECT DATE(time_out) AS date, COUNT(*) AS time_out_count
        FROM time_logs
        WHERE time_out >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE(time_out)
        ORDER BY DATE(time_out);
    ''')
    time_out_data = cursor.fetchall()

    # Debugging output
    print("SQL Query Executed for Time-Ins")
    print("Raw Time-In Data:", time_in_data)
    print("SQL Query Executed for Time-Outs")
    print("Raw Time-Out Data:", time_out_data)

    cursor.close()
    close_db_connection(connection)

    # Prepare data for the chart
    dates = sorted(set(row[0] for row in time_in_data) | set(row[0] for row in time_out_data))
    time_in_counts = [next((count for date, count in time_in_data if date == d), 0) for d in dates]
    time_out_counts = [next((count for date, count in time_out_data if date == d), 0) for d in dates]

    # Debugging output
    print("Dates:", dates)
    print("Time-In Counts:", time_in_counts)
    print("Time-Out Counts:", time_out_counts)

    return {
        'labels': [date.strftime('%Y-%m-%d') for date in dates],
        'timein': time_in_counts,
        'timeout': time_out_counts
    }
