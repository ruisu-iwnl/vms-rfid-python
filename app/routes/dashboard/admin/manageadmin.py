from flask import Blueprint, render_template, session
from app.routes.utils.forms import AddAdminForm
from app.models.database import get_cursor, close_db_connection

adminlist_bp = Blueprint('adminlist', __name__)

@adminlist_bp.route('/', defaults={'page': 1, 'sort_by': 'emp_no', 'order': 'asc'})
@adminlist_bp.route('/<int:page>/<string:sort_by>/<string:order>')
def adminlist(page, sort_by='emp_no', order='asc'):
    if not session.get('is_super_admin'): 
        return "Access denied. You are not authorized to view this page.", 403
    
    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        super_admin_features = True
    else:
        super_admin_features = False

    valid_columns = {'emp_no': 'a.employee_id', 'full_name': 'full_name', 'contactnumber': 'a.contactnumber', 'created_at': 'a.created_at'}

    sort_column = valid_columns.get(sort_by, 'a.employee_id')
    
    try:
        cursor, connection = get_cursor()
        
        cursor.execute(f"""
            SELECT a.employee_id AS emp_no, CONCAT(a.firstname, ' ', a.lastname) AS full_name, a.contactnumber, 
                a.email, a.created_at, a.profile_image
            FROM admin a
            ORDER BY {sort_column} {order}, a.employee_id
        """)

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
