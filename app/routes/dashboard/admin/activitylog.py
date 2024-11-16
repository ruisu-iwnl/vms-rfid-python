from flask import Blueprint, render_template, request, make_response,session
from app.routes.utils.session import check_access
from app.routes.models.database import get_cursor, close_db_connection
import csv
from io import StringIO

activitylog_bp = Blueprint('activitylog', __name__)

@activitylog_bp.route('/', defaults={'page': 1, 'sort_by': 'activity_timestamp', 'order': 'desc'})
@activitylog_bp.route('/<int:page>/<string:sort_by>/<string:order>')
def activitylog(page, sort_by='activity_timestamp', order='desc'):
    response = check_access('admin')
    if response:
        return response
    
    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        print("This admin is a super admin.")

        super_admin_features = True
    else:
        print("This admin is NOT a super admin.")
        super_admin_features = False

    valid_columns = {'activity_timestamp': 'activity_timestamp', 'activity_type': 'activity_type', 'account_type': 'account_type'}
    
    sort_column = valid_columns.get(sort_by, 'activity_timestamp')
    sort_order = 'ASC' if order == 'asc' else 'DESC'
    
    cursor, connection = get_cursor()

    # Updated query excluding the 'account_id' column
    query = f"""
        SELECT 
            CASE
                WHEN al.account_type = 'Admin' THEN a.firstname
                ELSE u.firstname
            END AS firstname,
            CASE
                WHEN al.account_type = 'Admin' THEN a.lastname
                ELSE u.lastname
            END AS lastname,
            CASE
                WHEN al.account_type = 'Admin' THEN a.employee_id
                ELSE u.emp_no
            END AS employee_id,
            al.account_type, 
            al.activity_type, 
            al.activity_timestamp
        FROM (
            SELECT 'Admin' AS account_type, activity_type, activity_timestamp, admin_id AS user_id
            FROM admin_activity_log
            UNION ALL
            SELECT 'User' AS account_type, activity_type, activity_timestamp, user_id AS user_id
            FROM user_activity_log
        ) AS al
        LEFT JOIN admin a ON al.account_type = 'Admin' AND a.admin_id = al.user_id
        LEFT JOIN user u ON al.account_type = 'User' AND u.user_id = al.user_id
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

    return render_template('dashboard/admin/activitylog.html', records=records, page=page, total_pages=total_pages, sort_by=sort_by, order=order, super_admin_features=super_admin_features )

@activitylog_bp.route('/download_csv/<string:sort_by>/<string:order>')
def download_csv(sort_by='activity_timestamp', order='desc'):
    valid_columns = {'activity_timestamp': 'activity_timestamp', 'activity_type': 'activity_type', 'account_type': 'account_type'}
    
    sort_column = valid_columns.get(sort_by, 'activity_timestamp')
    sort_order = 'ASC' if order == 'asc' else 'DESC'
    
    cursor, connection = get_cursor()

    query = f"""
        SELECT 
            CASE
                WHEN al.account_type = 'Admin' THEN a.firstname
                ELSE u.firstname
            END AS firstname,
            CASE
                WHEN al.account_type = 'Admin' THEN a.lastname
                ELSE u.lastname
            END AS lastname,
            CASE
                WHEN al.account_type = 'Admin' THEN a.employee_id
                ELSE u.emp_no
            END AS employee_id,
            al.account_type, 
            al.activity_type, 
            al.activity_timestamp
        FROM (
            SELECT 'Admin' AS account_type, activity_type, activity_timestamp, admin_id AS user_id
            FROM admin_activity_log
            UNION ALL
            SELECT 'User' AS account_type, activity_type, activity_timestamp, user_id AS user_id
            FROM user_activity_log
        ) AS al
        LEFT JOIN admin a ON al.account_type = 'Admin' AND a.admin_id = al.user_id
        LEFT JOIN user u ON al.account_type = 'User' AND u.user_id = al.user_id
        ORDER BY {sort_column} {sort_order};
    """

    cursor.execute(query)
    records = cursor.fetchall()
    close_db_connection(connection)

    output = StringIO()
    writer = csv.writer(output)

    # Write metadata and headers
    writer.writerow(['Design and Development'])
    writer.writerow(['of TimeGuard: A Time Tracking Web System using RFID Technologies'])
    writer.writerow([])  # Blank line
    
    writer.writerow(['First Name', 'Last Name', 'Employee ID', 'Account Type', 'Activity Type', 'Timestamp'])  

    # Write data rows
    for record in records:
        writer.writerow(record)

    output.seek(0)

    # Create CSV response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=activity_log.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    return response
