from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.routes.utils.forms import Admin_AddUserVehicleForm
from app.routes.utils.activity_log import log_login_activity 
from app.routes.dashboard.admin.modals.addvehicle_utils import add_vehicle_to_db, get_users
from app.models.database import get_db_connection, close_db_connection, get_cars_cursor

user_vehicle_bp = Blueprint('user_vehicle', __name__, url_prefix='/admin/addvehicle')

@user_vehicle_bp.route('/search_makes', methods=['GET'])
def search_makes():
    makes = set()
    
    try:
        cursor, connection = get_cars_cursor()
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            if 'make' in columns:
                cursor.execute(f"SELECT DISTINCT make FROM {table_name}")
                for (make,) in cursor.fetchall():
                    makes.add(make)

        close_db_connection(connection)
    except Exception as e:
        print(f"Error fetching makes: {e}")

    return jsonify(sorted(makes))

@user_vehicle_bp.route('/search_models', methods=['GET'])
def search_models():
    make = request.args.get('make', '')
    models = set()

    if not make:
        return jsonify(list(models))

    try:
        cursor, connection = get_cars_cursor()
        for year in range(1992, 2027):
            table_name = f"`{year}`"
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            if 'make' in columns and 'model' in columns:
                cursor.execute(f"SELECT DISTINCT model FROM {table_name} WHERE make = %s", (make,))
                for (model,) in cursor.fetchall():
                    models.add(model)

        close_db_connection(connection)
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
    vehicle_form = Admin_AddUserVehicleForm()
    admin_id = session.get('admin_id')

    vehicle_form.user_id.choices = [(user[0], user[1]) for user in get_users()]

    if vehicle_form.validate_on_submit():
        user_id = vehicle_form.user_id.data
        make = request.form.get('make')  
        model = request.form.get('model')  
        license_plate = vehicle_form.license_plate.data
        rfid_number = vehicle_form.rfid_number.data

        print(f"Submitting vehicle: user_id={user_id}, make={make}, model={model}, license_plate={license_plate}, rfid_number={rfid_number}")

        if not user_id or not make or not model or not license_plate or not rfid_number:
            flash("All fields are required.", "danger")
            print("Validation failed: All fields are required.")
            return redirect(url_for('user_vehicle.uservehicle'))

        success = add_vehicle_to_db(user_id, make, model, license_plate, rfid_number)

        if success:
            log_login_activity(admin_id, 'Admin', f'Added vehicle and RFID to User ID {user_id}')
            flash('Vehicle added successfully!', 'success')
            print("Vehicle added successfully.")
        else:
            flash("Failed to add vehicle.", "danger")
            print("Failed to add vehicle to the database.")

    unique_errors = set()
    for errors in vehicle_form.errors.values():
        unique_errors.update(errors)

    for error in unique_errors:
        flash(error, "danger")
        print(f"Error: {error}")

    return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))
