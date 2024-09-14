from flask import Blueprint, request, jsonify, render_template,session

timeinout_bp = Blueprint('timeinout', __name__, url_prefix='/dashboard/timeinout')

@timeinout_bp.route('/', defaults={'page': 1})
@timeinout_bp.route('/<int:page>')
def timeinout(page):
    records = [
        {'date': '2024-09-01', 'time_in': '08:00', 'time_out': '17:00', 'employee_id': 'E001', 'name': 'John Doe', 'phone_number': '555-0100'},
        {'date': '2024-09-02', 'time_in': '09:00', 'time_out': '18:00', 'employee_id': 'E002', 'name': 'Jane Smith', 'phone_number': '555-0101'},
        {'date': '2024-09-03', 'time_in': '08:30', 'time_out': '17:30', 'employee_id': 'E003', 'name': 'Alice Johnson', 'phone_number': '555-0102'},
        {'date': '2024-09-04', 'time_in': '08:15', 'time_out': '17:15', 'employee_id': 'E004', 'name': 'Bob Brown', 'phone_number': '555-0103'},
        {'date': '2024-09-05', 'time_in': '09:00', 'time_out': '18:00', 'employee_id': 'E005', 'name': 'Carol White', 'phone_number': '555-0104'},
        {'date': '2024-09-06', 'time_in': '08:00', 'time_out': '16:00', 'employee_id': 'E006', 'name': 'David Green', 'phone_number': '555-0105'},
        {'date': '2024-09-07', 'time_in': '09:00', 'time_out': '17:00', 'employee_id': 'E007', 'name': 'Eva Black', 'phone_number': '555-0106'},
        {'date': '2024-09-08', 'time_in': '08:45', 'time_out': '17:15', 'employee_id': 'E008', 'name': 'Frank Blue', 'phone_number': '555-0107'},
        {'date': '2024-09-09', 'time_in': '09:30', 'time_out': '18:00', 'employee_id': 'E009', 'name': 'Grace Red', 'phone_number': '555-0108'},
        {'date': '2024-09-10', 'time_in': '08:00', 'time_out': '17:00', 'employee_id': 'E010', 'name': 'Henry Grey', 'phone_number': '555-0109'},
        {'date': '2024-09-11', 'time_in': '09:00', 'time_out': '18:00', 'employee_id': 'E011', 'name': 'Ivy Pink', 'phone_number': '555-0110'},
        {'date': '2024-09-12', 'time_in': '08:30', 'time_out': '17:30', 'employee_id': 'E012', 'name': 'Jack Orange', 'phone_number': '555-0111'},
        {'date': '2024-09-13', 'time_in': '08:15', 'time_out': '17:15', 'employee_id': 'E013', 'name': 'Kathy Purple', 'phone_number': '555-0112'},
        {'date': '2024-09-14', 'time_in': '09:00', 'time_out': '18:00', 'employee_id': 'E014', 'name': 'Louis Gold', 'phone_number': '555-0113'},
        {'date': '2024-09-15', 'time_in': '08:00', 'time_out': '16:00', 'employee_id': 'E015', 'name': 'Mia Silver', 'phone_number': '555-0114'},
        {'date': '2024-09-16', 'time_in': '09:00', 'time_out': '17:00', 'employee_id': 'E016', 'name': 'Nick Bronze', 'phone_number': '555-0115'},
        {'date': '2024-09-17', 'time_in': '08:45', 'time_out': '17:15', 'employee_id': 'E017', 'name': 'Olivia White', 'phone_number': '555-0116'},
        {'date': '2024-09-18', 'time_in': '09:30', 'time_out': '18:00', 'employee_id': 'E018', 'name': 'Paul Black', 'phone_number': '555-0117'},
        {'date': '2024-09-19', 'time_in': '08:00', 'time_out': '17:00', 'employee_id': 'E019', 'name': 'Quinn Red', 'phone_number': '555-0118'},
        {'date': '2024-09-20', 'time_in': '09:00', 'time_out': '18:00', 'employee_id': 'E020', 'name': 'Riley Blue', 'phone_number': '555-0119'},
        {'date': '2024-09-21', 'time_in': '08:30', 'time_out': '17:30', 'employee_id': 'E021', 'name': 'Samantha Green', 'phone_number': '555-0120'}
    ]

    per_page = 5
    total_records = len(records)
    total_pages = (total_records + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_records = records[start:end]

    print(f"Session active in timelogs: {session}")
    return render_template('dashboard/admin/timeinout.html', records=paginated_records, page=page, total_pages=total_pages)

@timeinout_bp.route('/process_rfid', methods=['POST'])
def process_rfid():
    data = request.get_json()
    rfid_number = data.get('rfid', '').strip()

    if rfid_number:
        print(f'RFID Number scanned: {rfid_number}')  # Handle the RFID number (e.g., save to database)
        response = {'rfid_number': rfid_number}
    else:
        response = {'rfid_number': 'RFID not detected'}

    return jsonify(response)