from flask import Blueprint, render_template, request
from app.routes.utils.session import check_access
from app.routes.models.database import get_cursor, close_db_connection

activitylog_bp = Blueprint('activitylog', __name__)

@activitylog_bp.route('/', defaults={'page': 1, 'sort_by': 'activity_timestamp', 'order': 'desc'})
@activitylog_bp.route('/<int:page>/<string:sort_by>/<string:order>')
def activitylog(page, sort_by='activity_timestamp', order='desc'):
    response = check_access('admin')
    if response:
        return response

    valid_columns = {'activity_timestamp': 'activity_timestamp', 'activity_type': 'activity_type', 'account_type': 'account_type', 'account_id': 'account_id'}
    
    sort_column = valid_columns.get(sort_by, 'activity_timestamp')
    sort_order = 'ASC' if order == 'asc' else 'DESC'
    
    cursor, connection = get_cursor()

    # Query to get admin and user activity logs with sorting
    query = f"""
        SELECT account_type, account_id, activity_type, activity_timestamp
        FROM (
            SELECT 'Admin' AS account_type, admin_id AS account_id, activity_type, activity_timestamp
            FROM admin_activity_log
            UNION ALL
            SELECT 'User' AS account_type, user_id AS account_id, activity_type, activity_timestamp
            FROM user_activity_log
        ) AS combined_activity
        ORDER BY {sort_column} {sort_order}
        LIMIT %s OFFSET %s;
    """

    per_page = 5
    offset = (page - 1) * per_page

    cursor.execute(query, (per_page, offset))
    records = cursor.fetchall()

    # Count total records for pagination
    count_query = """
        SELECT COUNT(*) FROM (
            SELECT admin_id FROM admin_activity_log
            UNION ALL
            SELECT user_id FROM user_activity_log
        ) AS total_activity;
    """
    cursor.execute(count_query)
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + per_page - 1) // per_page

    close_db_connection(connection)

    return render_template('dashboard/admin/activitylog.html', records=records, page=page, total_pages=total_pages, sort_by=sort_by, order=order)
