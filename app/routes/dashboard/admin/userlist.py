from flask import Blueprint, render_template, session
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

    valid_columns = {'emp_no': 'u.emp_no', 'full_name': 'full_name', 'contactnumber': 'u.contactnumber', 'vehicle_count': 'vehicle_count', 'created_at': 'u.created_at'}
    
    sort_column = valid_columns.get(sort_by, 'u.emp_no')
    
    form = AddUserForm()
    vehicle_form = Admin_AddUserVehicleForm() 
    
    try:
        cursor, connection = get_cursor()
        
        cursor.execute(f"""
            SELECT u.emp_no, CONCAT(u.firstname, ' ', u.lastname) AS full_name, u.contactnumber, 
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                COUNT(v.vehicle_id) AS vehicle_count, u.created_at
            FROM user u
            LEFT JOIN vehicle v ON u.user_id = v.user_id
            GROUP BY u.user_id
            ORDER BY {sort_column} {order}, u.emp_no
        """)


        users = cursor.fetchall()
        
        per_page = 5
        total_users = len(users)
        total_pages = (total_users + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_users = users[start:end]

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return "An error occurred while fetching user data", 500

    finally:
        cursor.close()
        close_db_connection(connection)

    return render_template('dashboard/admin/userlist.html', 
                           users=paginated_users, 
                           page=page, 
                           total_pages=total_pages, 
                           sort_by=sort_by, 
                           order=order, 
                           form=form,
                           vehicle_form=vehicle_form)
