from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.routes.utils.forms import AddAdminForm
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.activity_log import log_login_activity 
adminlist_bp = Blueprint('adminlist', __name__)

@adminlist_bp.route('/', defaults={'page': 1, 'sort_by': 'emp_no', 'order': 'asc'})
@adminlist_bp.route('/<int:page>/<string:sort_by>/<string:order>')
def adminlist(page, sort_by='emp_no', order='asc'):
    if not session.get('is_super_admin'): 
        return "Access denied. You are not authorized to view this page.", 403
    
    is_super_admin = session.get('is_super_admin', False)
    super_admin_features = is_super_admin

    valid_columns = {'emp_no': 'a.employee_id', 'full_name': 'full_name', 'contactnumber': 'a.contactnumber', 'created_at': 'a.created_at'}
    sort_column = valid_columns.get(sort_by, 'a.employee_id')

    logged_in_admin_email = session.get('email')

    try:
        cursor, connection = get_cursor()
        
        cursor.execute(f"""
            SELECT a.admin_id, a.employee_id AS emp_no, CONCAT(a.firstname, ' ', a.lastname) AS full_name, 
                a.contactnumber, a.email, a.created_at, a.profile_image, a.is_super_admin
            FROM admin a
            WHERE a.deleted_at IS NULL
            AND a.email != %s  -- Exclude the logged-in admin
            ORDER BY {sort_column} {order}, a.employee_id
        """, (logged_in_admin_email,))


        admins = cursor.fetchall()
        
        per_page = 5
        total_admins = len(admins)
        total_pages = (total_admins + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_admins = admins[start:end]

    except Exception as e:
        print(f"Error fetching admin data: {e}")
        return "An error occurred while fetching admin data", 500

    finally:
        cursor.close()
        close_db_connection(connection)

    form = AddAdminForm()

    return render_template('dashboard/admin/manageadmin.html', 
                           admins=paginated_admins, 
                           page=page, 
                           total_pages=total_pages, 
                           sort_by=sort_by, 
                           order=order, 
                           super_admin_features=super_admin_features,
                           form=form)

@adminlist_bp.route('/delete_admin/<int:admin_id>', methods=['POST'])
def delete_admin(admin_id):
    if not session.get('is_super_admin'):
        return "Access denied. You are not authorized to perform this action.", 403

    try:
        cursor, connection = get_cursor()

        cursor.execute("""
            UPDATE admin
            SET deleted_at = NOW()
            WHERE admin_id = %s AND deleted_at IS NULL
        """, (admin_id,))

        # Commit the changes
        connection.commit()

        # Flash a success message
        flash('Admin has been soft-deleted.', 'success')
    except Exception as e:
        print(f"Error deleting admin: {e}")
        flash('An error occurred while deleting the admin.', 'error')
        return redirect(url_for('adminlist.adminlist', page=1))
    finally:
        cursor.close()
        close_db_connection(connection)

    return redirect(url_for('adminlist.adminlist', page=1))


@adminlist_bp.route('/toggle_super_admin/<int:admin_id>', methods=['POST'])
def toggle_super_admin(admin_id):
    if not session.get('is_super_admin'):
        return "Access denied. You are not authorized to perform this action.", 403

    try:
        cursor, connection = get_cursor()

        # Get current super admin status
        cursor.execute("SELECT is_super_admin FROM admin WHERE admin_id = %s", (admin_id,))
        current_status = cursor.fetchone()

        if current_status is None:
            return "Admin not found", 404

        print(f"Current status of super admin for admin {admin_id}: {current_status[0]}")  # Debugging output

        # Toggle the super admin status (flip 1 to 0 or 0 to 1)
        is_super_admin = 0 if current_status[0] == 1 else 1  # Flip the current status
        print(f"Toggled super admin status for admin {admin_id} to {is_super_admin}")

        # Update the super admin status in the database
        cursor.execute("""
            UPDATE admin
            SET is_super_admin = %s
            WHERE admin_id = %s
        """, (is_super_admin, admin_id))
        connection.commit()

        # Log the activity
        logged_in_admin_email = session.get('email')
        cursor.execute("SELECT admin_id FROM admin WHERE email = %s", (logged_in_admin_email,))
        logged_in_admin_id = cursor.fetchone()[0]

        log_login_activity(logged_in_admin_id, 'Admin', f"Toggled Super Admin Status for admin {admin_id}")

        print(f"Super admin status for admin {admin_id} updated to {is_super_admin}")

        # Redirect to reload the page and show the updated status
        return redirect(url_for('adminlist.adminlist', page=1))

    except Exception as e:
        print(f"Error toggling super admin status: {e}")
        return "An error occurred while updating the admin's status", 500

    finally:
        cursor.close()
        close_db_connection(connection)
