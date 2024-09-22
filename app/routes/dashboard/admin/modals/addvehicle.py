from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.routes.utils.forms import Admin_AddUserVehicleForm
from app.routes.utils.activity_log import log_login_activity 
from app.routes.dashboard.admin.modals.addvehicle_utils import add_vehicle_to_db, get_users
from app.models.database import get_db_connection, close_db_connection, get_cars_cursor

user_vehicle_bp = Blueprint('user_vehicle', __name__, url_prefix='/admin/addvehicle')

@user_vehicle_bp.route('/search_makes', methods=['GET'])
def search_makes():
    query = request.args.get('query', '')
    makes = set()

    if not query:
        print("No query provided for make search.")
        return jsonify(list(makes))

    print(f"Searching for makes with query: {query}")

    try:
        cursor, connection = get_cars_cursor()  
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            print(f"Querying table: {table_name} for makes matching '{query}'")
            cursor.execute(f"SELECT DISTINCT make FROM {table_name} WHERE make LIKE %s", (f'%{query}%',))
            for (make,) in cursor.fetchall():
                print(f"Found make: {make}")
                makes.add(make)

        close_db_connection(connection)
        print(f"Total unique makes found: {len(makes)}")
    except Exception as e:
        print(f"Error fetching makes: {e}")

    return jsonify(sorted(makes))

@user_vehicle_bp.route('/search_models', methods=['GET'])
def search_models():
    query = request.args.get('query', '')
    models = set()

    if not query:
        print("No query provided for model search.")
        return jsonify(list(models))

    print(f"Searching for models with query: {query}")

    try:
        cursor, connection = get_cars_cursor() 
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            print(f"Querying table: {table_name} for models matching '{query}'")
            cursor.execute(f"SELECT DISTINCT model FROM {table_name} WHERE model LIKE %s", (f'%{query}%',))
            for (model,) in cursor.fetchall():
                print(f"Found model: {model}")
                models.add(model)

        close_db_connection(connection)
        print(f"Total unique models found: {len(models)}")
    except Exception as e:
        print(f"Error fetching models: {e}")

    return jsonify(sorted(models))


@user_vehicle_bp.route('/search_users', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT user_id, firstname, lastname
        FROM user 
        WHERE firstname LIKE %s OR lastname LIKE %s OR user_id LIKE %s
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))

    users = cursor.fetchall()
    close_db_connection(conn)

    return jsonify(users)

@user_vehicle_bp.route('/', methods=['GET', 'POST'])
def uservehicle():
    print("Handling request for add vehicle...")
    vehicle_form = Admin_AddUserVehicleForm()  

    vehicle_form.user_id.choices = [(user[0], user[1]) for user in get_users()]
    print(f"Form user_id choices set: {vehicle_form.user_id.choices}")

    admin_id = session.get('admin_id')

    if vehicle_form.validate_on_submit():
        print("Form validated and submitted.")
        user_id = vehicle_form.user_id.data
        make = vehicle_form.make.data
        model = vehicle_form.model.data
        license_plate = vehicle_form.license_plate.data
        rfid_number = vehicle_form.rfid_number.data

        print(f"Form data: user_id={user_id}, make={make}, model={model}, license_plate={license_plate}, rfid_number={rfid_number}")

        if not user_id or not make or not model or not license_plate:
            flash("All fields except RFID are required.", "danger")
            return redirect(url_for('user_vehicle.uservehicle'))

        success = add_vehicle_to_db(user_id, make, model, license_plate, rfid_number)

        if success:
            log_login_activity(admin_id, 'Admin', f'Added vehicle and RFID to User ID {user_id}')
            flash('Vehicle added successfully!', 'success')
            print("Redirecting to user list...")
            return redirect(url_for('userlist.userlist'))
        else:
            print("Add vehicle failed, staying on the same page.")
            return redirect(url_for('user_vehicle.uservehicle'))

    print("Form did not validate")
    print(f"Form errors: {vehicle_form.errors}")

    unique_errors = set()
    for errors in vehicle_form.errors.values():
        unique_errors.update(errors)

    for errors in unique_errors:
        flash

    return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))