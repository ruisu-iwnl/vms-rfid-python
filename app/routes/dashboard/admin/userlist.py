from flask import Blueprint, render_template

userlist_bp = Blueprint('userlist', __name__)

@userlist_bp.route('/', defaults={'page': 1})
@userlist_bp.route('/<int:page>')
def userlist(page):
    # Sample data for demonstration. Replace this with your actual data source.
    users = [
        {'employee_number': '001', 'full_name': 'John Doe', 'contact_number': '555-0100', 'vehicle': 'Car'},
        {'employee_number': '002', 'full_name': 'Jane Smith', 'contact_number': '555-0101', 'vehicle': 'Bike'},
        {'employee_number': '003', 'full_name': 'Alice Johnson', 'contact_number': '555-0102', 'vehicle': 'Truck'},
        {'employee_number': '004', 'full_name': 'Bob Brown', 'contact_number': '555-0103', 'vehicle': 'Van'},
        {'employee_number': '005', 'full_name': 'Carol White', 'contact_number': '555-0104', 'vehicle': 'Car'},
        {'employee_number': '006', 'full_name': 'David Green', 'contact_number': '555-0105', 'vehicle': 'Bike'},
        {'employee_number': '007', 'full_name': 'Eva Black', 'contact_number': '555-0106', 'vehicle': 'Truck'},
        {'employee_number': '008', 'full_name': 'Frank Blue', 'contact_number': '555-0107', 'vehicle': 'Van'},
        {'employee_number': '009', 'full_name': 'Grace Red', 'contact_number': '555-0108', 'vehicle': 'Car'},
        {'employee_number': '010', 'full_name': 'Henry Grey', 'contact_number': '555-0109', 'vehicle': 'Bike'},
        {'employee_number': '011', 'full_name': 'Ivy Pink', 'contact_number': '555-0110', 'vehicle': 'Truck'},
        {'employee_number': '012', 'full_name': 'Jack Orange', 'contact_number': '555-0111', 'vehicle': 'Van'},
        {'employee_number': '013', 'full_name': 'Kathy Purple', 'contact_number': '555-0112', 'vehicle': 'Car'},
        {'employee_number': '014', 'full_name': 'Louis Gold', 'contact_number': '555-0113', 'vehicle': 'Bike'},
        {'employee_number': '015', 'full_name': 'Mia Silver', 'contact_number': '555-0114', 'vehicle': 'Truck'},
        {'employee_number': '016', 'full_name': 'Nick Bronze', 'contact_number': '555-0115', 'vehicle': 'Van'},
        {'employee_number': '017', 'full_name': 'Olivia White', 'contact_number': '555-0116', 'vehicle': 'Car'},
        {'employee_number': '018', 'full_name': 'Paul Black', 'contact_number': '555-0117', 'vehicle': 'Bike'},
        {'employee_number': '019', 'full_name': 'Quinn Red', 'contact_number': '555-0118', 'vehicle': 'Truck'},
        {'employee_number': '020', 'full_name': 'Riley Blue', 'contact_number': '555-0119', 'vehicle': 'Van'},
        {'employee_number': '021', 'full_name': 'Samantha Green', 'contact_number': '555-0120', 'vehicle': 'Car'}
    ]


    per_page = 5
    total_users = len(users)
    total_pages = (total_users + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]

    return render_template('dashboard/admin/userlist.html', users=paginated_users, page=page, total_pages=total_pages)
