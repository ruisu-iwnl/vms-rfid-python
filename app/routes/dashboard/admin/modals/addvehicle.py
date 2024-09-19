from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.models.database import get_db_connection, close_db_connection
from app.routes.utils.forms import Admin_AddUserVehicleForm
from app.routes.utils.activity_log import log_login_activity  
import mysql.connector

user_vehicle_bp = Blueprint('user_vehicle', __name__, url_prefix='/admin/addvehicle')

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

def get_users():
    print("Fetching users from the database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, firstname FROM user') 
    users = cursor.fetchall()
    close_db_connection(conn)
    print(f"Users fetched: {users}")
    return users

def add_vehicle_to_db(user_id, model, license_plate, rfid_number):
    print(f"Adding vehicle to database: user_id={user_id}, model={model}, license_plate={license_plate}, rfid_number={rfid_number}")
    conn = get_db_connection()
    cursor = conn.cursor()
    success = False
    
    try:
        cursor.execute('INSERT INTO vehicle (user_id, model, licenseplate) VALUES (%s, %s, %s)', 
                       (user_id, model, license_plate))
        vehicle_id = cursor.lastrowid
        
        cursor.execute('INSERT INTO rfid (vehicle_id, rfid_no) VALUES (%s, %s)', 
                       (vehicle_id, rfid_number))
        conn.commit()
        print("Vehicle and RFID data successfully added.")
        success = True
    except mysql.connector.IntegrityError as e:
        if e.errno == 1062:  
            flash("This license plate or RFID number is already registered.", "danger")
        else:
            flash(f"Database error: {e}", "danger")
        conn.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "danger")
        print(f"Exception occurred: {e}")
    finally:
        cursor.close()
        close_db_connection(conn)
    
    return success

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
        model = vehicle_form.model.data
        license_plate = vehicle_form.license_plate.data
        rfid_number = vehicle_form.rfid_number.data

        print(f"Form data: user_id={user_id}, model={model}, license_plate={license_plate}, rfid_number={rfid_number}")

        if not user_id or not model or not license_plate or not rfid_number:
            flash("All fields are required.", "danger")
            return redirect(url_for('user_vehicle.uservehicle'))

        success = add_vehicle_to_db(user_id, model, license_plate, rfid_number)

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

    for error in unique_errors:
        flash(error, 'danger')

    return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))
