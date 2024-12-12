from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.routes.utils.session import check_access
from app.routes.utils.forms import AddUserForm, Admin_AddUserVehicleForm
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.mail_helper import send_approved_notification, send_deny_notification

userlist_bp = Blueprint('userlist', __name__)

@userlist_bp.route('/', defaults={'approved_page': 1, 'unapproved_page': 1, 'sort_by': 'emp_no', 'order': 'asc'})
@userlist_bp.route('/<int:approved_page>/<int:unapproved_page>/<string:sort_by>/<string:order>')
def userlist(approved_page, unapproved_page, sort_by='emp_no', order='asc'):
    response = check_access('admin')
    
    if response:
        return response

    is_super_admin = session.get('is_super_admin', False)
    super_admin_features = is_super_admin

    valid_columns = {'emp_no': 'u.emp_no', 'full_name': 'full_name', 'contactnumber': 'u.contactnumber', 
                     'vehicle_count': 'vehicle_count', 'created_at': 'u.created_at'}
    
    sort_column = valid_columns.get(sort_by, 'u.emp_no')
    
    form = AddUserForm()
    vehicle_form = Admin_AddUserVehicleForm() 
    
    try:
        cursor, connection = get_cursor()

        # Query for approved users (including ORCR and Driver License)
        cursor.execute(f"""
            SELECT u.emp_no, CONCAT(u.firstname, ' ', u.lastname) AS full_name, u.contactnumber, 
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                COUNT(v.vehicle_id) AS vehicle_count, u.created_at, u.profile_image, 
                ud.orcr, ud.driverlicense
            FROM user u
            LEFT JOIN vehicle v ON u.user_id = v.user_id
            LEFT JOIN user_documents ud ON u.user_id = ud.user_id  # Joining with user_documents
            WHERE u.is_approved = 1 AND u.deleted_at IS NULL
            GROUP BY u.user_id
            ORDER BY {sort_column} {order}, u.emp_no
        """)
        approved_users = cursor.fetchall()

        # Query for unapproved users (including ORCR and Driver License)
        cursor.execute(f"""
            SELECT u.emp_no, CONCAT(u.firstname, ' ', u.lastname) AS full_name, u.contactnumber, 
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                COUNT(v.vehicle_id) AS vehicle_count, u.created_at, u.profile_image, 
                ud.orcr, ud.driverlicense
            FROM user u
            LEFT JOIN vehicle v ON u.user_id = v.user_id
            LEFT JOIN user_documents ud ON u.user_id = ud.user_id  # Joining with user_documents
            WHERE u.is_approved = 0 AND u.deleted_at IS NULL
            GROUP BY u.user_id
            ORDER BY {sort_column} {order}, u.emp_no
        """)
        unapproved_users = cursor.fetchall()

        # Pagination for approved users
        per_page = 5
        total_approved_users = len(approved_users)
        total_pages = (total_approved_users + per_page - 1) // per_page
        approved_start = (approved_page - 1) * per_page
        approved_end = approved_start + per_page
        paginated_approved_users = approved_users[approved_start:approved_end]

        # Pagination for unapproved users
        total_unapproved_users = len(unapproved_users)
        unapproved_total_pages = (total_unapproved_users + per_page - 1) // per_page
        unapproved_start = (unapproved_page - 1) * per_page
        unapproved_end = unapproved_start + per_page
        paginated_unapproved_users = unapproved_users[unapproved_start:unapproved_end]

        print("Approved Users:", approved_users)
        print("Unapproved Users:", unapproved_users)

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return "An error occurred while fetching user data", 500

    finally:
        cursor.close()
        close_db_connection(connection)

    return render_template('dashboard/admin/userlist.html', 
        approved_users=paginated_approved_users, 
        unapproved_users=paginated_unapproved_users, 
        approved_page=approved_page, 
        unapproved_page=unapproved_page,
        total_approved_pages=total_pages,
        unapproved_total_pages=unapproved_total_pages,  # Ensure this is passed here
        sort_by=sort_by, 
        order=order, 
        form=form,
        vehicle_form=vehicle_form,
        super_admin_features=super_admin_features)

@userlist_bp.route('/confirm/<string:emp_no>', methods=['POST'])
def confirm_user(emp_no):
    try:
        cursor, connection = get_cursor()

        cursor.execute("SELECT email FROM user WHERE emp_no = %s", (emp_no,))
        result = cursor.fetchone()

        if result:
            email = result[0]

            send_approved_notification(email)

            cursor.execute("""
                UPDATE user
                SET is_approved = 1
                WHERE emp_no = %s
            """, (emp_no,))
            connection.commit()

            flash('User approved successfully and approve notification sent!', 'success')
        else:
            flash('User not found.', 'error')

        return redirect(url_for('userlist.userlist'))

    except Exception as e:
        print(f"Error confirming user: {e}")
        return "An error occurred while confirming the user", 500

    finally:
        cursor.close()
        close_db_connection(connection)

@userlist_bp.route('/deny/<string:emp_no>', methods=['POST'])
def deny_user(emp_no):
    try:
        cursor, connection = get_cursor()

        cursor.execute("""
            UPDATE user
            SET deleted_at = NOW()
            WHERE emp_no = %s
        """, (emp_no,))

        cursor.execute("""
            UPDATE vehicle
            SET deleted_at = NOW()
            WHERE user_id IN (SELECT user_id FROM user WHERE emp_no = %s)
        """, (emp_no,))

        connection.commit()

        cursor.execute("SELECT email FROM user WHERE emp_no = %s", (emp_no,))
        result = cursor.fetchone()
        if result:
            send_deny_notification(result[0])

        flash('User and their data soft-deleted successfully and denial notification sent!', 'success')

        return redirect(url_for('userlist.userlist')) 

    except Exception as e:
        print(f"Error denying user: {e}")
        return "An error occurred while denying the user", 500

    finally:
        cursor.close()
        close_db_connection(connection)
