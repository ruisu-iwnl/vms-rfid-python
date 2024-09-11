from flask import Blueprint, render_template

activitylog_bp = Blueprint('activitylog', __name__)

@activitylog_bp.route('/', defaults={'page': 1})
@activitylog_bp.route('/<int:page>')
def activitylog(page):
    records = [
        {'activity_id': 1, 'user_id': 101, 'activity_type': 'Login', 'timestamp': '2024-09-01 08:00:00'},
        {'activity_id': 2, 'user_id': 102, 'activity_type': 'Logout', 'timestamp': '2024-09-01 09:00:00'},
        {'activity_id': 3, 'user_id': 103, 'activity_type': 'Login', 'timestamp': '2024-09-02 10:00:00'},
        {'activity_id': 4, 'user_id': 104, 'activity_type': 'Upload', 'timestamp': '2024-09-02 11:00:00'},
        {'activity_id': 5, 'user_id': 105, 'activity_type': 'Download', 'timestamp': '2024-09-03 12:00:00'},
        {'activity_id': 6, 'user_id': 106, 'activity_type': 'Login', 'timestamp': '2024-09-03 13:00:00'},
        {'activity_id': 7, 'user_id': 107, 'activity_type': 'Logout', 'timestamp': '2024-09-04 14:00:00'},
        {'activity_id': 8, 'user_id': 108, 'activity_type': 'Login', 'timestamp': '2024-09-04 15:00:00'},
        {'activity_id': 9, 'user_id': 109, 'activity_type': 'Upload', 'timestamp': '2024-09-05 16:00:00'},
        {'activity_id': 10, 'user_id': 110, 'activity_type': 'Download', 'timestamp': '2024-09-05 17:00:00'},
        {'activity_id': 11, 'user_id': 111, 'activity_type': 'Login', 'timestamp': '2024-09-06 18:00:00'},
        {'activity_id': 12, 'user_id': 112, 'activity_type': 'Logout', 'timestamp': '2024-09-06 19:00:00'},
        {'activity_id': 13, 'user_id': 113, 'activity_type': 'Upload', 'timestamp': '2024-09-07 20:00:00'},
        {'activity_id': 14, 'user_id': 114, 'activity_type': 'Download', 'timestamp': '2024-09-07 21:00:00'},
        {'activity_id': 15, 'user_id': 115, 'activity_type': 'Login', 'timestamp': '2024-09-08 22:00:00'},
        {'activity_id': 16, 'user_id': 116, 'activity_type': 'Logout', 'timestamp': '2024-09-09 23:00:00'},
        {'activity_id': 17, 'user_id': 117, 'activity_type': 'Upload', 'timestamp': '2024-09-10 00:00:00'},
        {'activity_id': 18, 'user_id': 118, 'activity_type': 'Download', 'timestamp': '2024-09-10 01:00:00'},
        {'activity_id': 19, 'user_id': 119, 'activity_type': 'Login', 'timestamp': '2024-09-11 02:00:00'},
        {'activity_id': 20, 'user_id': 120, 'activity_type': 'Logout', 'timestamp': '2024-09-11 03:00:00'},
        {'activity_id': 21, 'user_id': 121, 'activity_type': 'Upload', 'timestamp': '2024-09-12 04:00:00'}
    ]

    per_page = 5
    total_records = len(records)
    total_pages = (total_records + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_records = records[start:end]

    return render_template('dashboard/admin/activitylog.html', records=paginated_records, page=page, total_pages=total_pages)
