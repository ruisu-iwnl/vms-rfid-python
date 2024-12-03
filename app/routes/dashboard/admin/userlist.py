from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.routes.utils.session import check_access
from app.routes.utils.forms import AddUserForm, Admin_AddUserVehicleForm
from app.models.database import get_cursor, close_db_connection

userlist_bp = Blueprint('userlist', __name__)

@userlist_bp.route('/', defaults={'page': 1, 'sort_by': 'emp_no', 'order': 'asc'})
@userlist_bp.route('/<int:page>/<string:sort_by>/<string:order>')
def userlist(page, sort_by='emp_no', order='asc'):
    response = check_access('admin')
    
    if response:
        return response

    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        super_admin_features = True
    else:
        super_admin_features = False

    valid_columns = {'emp_no': 'u.emp_no', 'full_name': 'full_name', 'contactnumber': 'u.contactnumber', 
                     'vehicle_count': 'vehicle_count', 'created_at': 'u.created_at'}
    
    sort_column = valid_columns.get(sort_by, 'u.emp_no')
    
    form = AddUserForm()
    vehicle_form = Admin_AddUserVehicleForm() 
    
    try:
        cursor, connection = get_cursor()

        # Query for approved users (excluding soft-deleted users)
        cursor.execute(f"""
            SELECT u.emp_no, CONCAT(u.firstname, ' ', u.lastname) AS full_name, u.contactnumber, 
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                COUNT(v.vehicle_id) AS vehicle_count, u.created_at, u.profile_image
            FROM user u
            LEFT JOIN vehicle v ON u.user_id = v.user_id
            WHERE u.is_approved = 1 AND u.deleted_at IS NULL
            GROUP BY u.user_id
            ORDER BY {sort_column} {order}, u.emp_no
        """)
        approved_users = cursor.fetchall()

        # Query for unapproved users (excluding soft-deleted users)
        cursor.execute(f"""
            SELECT u.emp_no, CONCAT(u.firstname, ' ', u.lastname) AS full_name, u.contactnumber, 
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                COUNT(v.vehicle_id) AS vehicle_count, u.created_at, u.profile_image
            FROM user u
            LEFT JOIN vehicle v ON u.user_id = v.user_id
            WHERE u.is_approved = 0 AND u.deleted_at IS NULL
            GROUP BY u.user_id
            ORDER BY {sort_column} {order}, u.emp_no
        """)
        unapproved_users = cursor.fetchall()

        # Pagination for approved users
        per_page = 5
        total_approved_users = len(approved_users)
        total_pages = (total_approved_users + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_approved_users = approved_users[start:end]

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
                           unapproved_users=unapproved_users, 
                           page=page, 
                           total_pages=total_pages, 
                           sort_by=sort_by, 
                           order=order, 
                           form=form,
                           vehicle_form=vehicle_form,
                           super_admin_features=super_admin_features)


@userlist_bp.route('/confirm/<string:emp_no>', methods=['POST'])
def confirm_user(emp_no):
    try:
        cursor, connection = get_cursor()

        # Update the user to approved (is_approved = 1) using emp_no
        cursor.execute("""
            UPDATE user
            SET is_approved = 1
            WHERE emp_no = %s
        """, (emp_no,))
        connection.commit()

        # Optionally, you can flash a success message
        flash('User approved successfully!', 'success')
        
        return redirect(url_for('userlist.userlist'))  # Redirect back to the user list page

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

        # Soft delete the user by setting the deleted_at field
        cursor.execute("""
            UPDATE user
            SET deleted_at = NOW()
            WHERE emp_no = %s
        """, (emp_no,))

        # Optionally, you can also soft delete the user's vehicles by setting a deleted_at field for vehicles
        # (If you choose to add a `deleted_at` column to the vehicle table too)
        cursor.execute("""
            UPDATE vehicle
            SET deleted_at = NOW()
            WHERE user_id IN (SELECT user_id FROM user WHERE emp_no = %s)
        """, (emp_no,))

        connection.commit()

        # Optionally, you can flash a success message
        flash('User and their data soft-deleted successfully!', 'success')

        return redirect(url_for('userlist.userlist'))  # Redirect back to the user list page

    except Exception as e:
        print(f"Error denying user: {e}")
        return "An error occurred while denying the user", 500

    finally:
        cursor.close()
        close_db_connection(connection)
