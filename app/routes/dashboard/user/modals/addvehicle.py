from flask import Blueprint, redirect, flash, request, url_for, session,jsonify
from app.routes.utils.forms import AddVehicleForm
import mysql.connector
from app.models.database import get_cursor, close_db_connection, get_cars_cursor
from app.routes.utils.session import check_access
from app.routes.utils.activity_log import log_login_activity

add_vehicle_bp = Blueprint('add_vehicle', __name__, url_prefix='/add_vehicle')

def is_rfid_valid(rfid_number):
    """Check if the RFID number exists in the system."""
    cursor, connection = get_cursor()
    cursor.execute('SELECT COUNT(*) FROM rfid WHERE rfid_no = %s', (rfid_number,))
    count = cursor.fetchone()[0]
    cursor.close()
    close_db_connection(connection)
    return count > 0

@add_vehicle_bp.route('/add', methods=['GET', 'POST'])
def add_vehicle():
    print("Entering add_vehicle route")

    response = check_access('user')
    if response:
        print("Unauthorized access detected, redirecting...")
        return response

    user_id = session.get('user_id')
    if not user_id:
        print("User ID is not set in the session. User might not be logged in.")
        flash("You need to be logged in to add a vehicle.", "danger")
        return redirect(url_for('main.index'))

    form = AddVehicleForm()

    if form.validate_on_submit():
        print("Form validated successfully")
        car_make = form.car_make.data  
        car_model = form.car_model.data
        plate_number = form.plate_number.data
        rfid_number = form.rfid_number.data

        cleaned_plate_number = plate_number.replace(" ", "").upper()

        print(f"Form data - Car Make: {car_make}, Car Model: {car_model}, Plate Number: {cleaned_plate_number}, RFID Number: {rfid_number}")

        try:
            cursor, connection = get_cursor()  
            print("Database connection established")

            if rfid_number and not is_rfid_valid(rfid_number):
                flash("The provided RFID number is not registered.", "danger")
                return redirect(url_for('vehicles.vehicles'))

            cursor.execute("SELECT vehicle_id FROM vehicle WHERE REPLACE(licenseplate, ' ', '') = %s", (cleaned_plate_number,))
            existing_vehicle = cursor.fetchone()
            if existing_vehicle:
                flash("This license plate is already registered.", "danger")
                return redirect(url_for('vehicles.vehicles'))

            cursor.execute(
                "INSERT INTO vehicle (user_id, licenseplate, make, model) VALUES (%s, %s, %s, %s)",
                (user_id, cleaned_plate_number, car_make, car_model)
            )

            vehicle_id = cursor.lastrowid
            print(f"Inserted vehicle ID: {vehicle_id}")

            if rfid_number:
                cursor.execute('SELECT vehicle_id FROM rfid WHERE rfid_no = %s', (rfid_number,))
                existing_rfid = cursor.fetchone()

                if existing_rfid and existing_rfid[0] is not None:
                    flash("This RFID number is already registered to a vehicle.", "danger")
                    return redirect(url_for('vehicles.vehicles'))

                cursor.execute("UPDATE rfid SET vehicle_id = %s WHERE rfid_no = %s", (vehicle_id, rfid_number))
                print(f"Updated RFID: {rfid_number}")

            connection.commit()
            flash("Vehicle added successfully", "success")
            print("Vehicle added successfully, redirecting...")

            # Log successful vehicle addition with details
            details = f"Added vehicle with Make: {car_make}, Model: {car_model}, RFID Number: {rfid_number}"
            log_login_activity(user_id, 'User', details)

            return redirect(url_for('vehicles.vehicles'))

        except mysql.connector.IntegrityError as e:
            print(f"Database integrity error: {e}")
            if e.errno == 1062:
                flash("An RFID number or license plate is already registered.", "danger")
            else:
                flash(f"Database error: {e}", "danger")
            return redirect(url_for('vehicles.vehicles'))

        except Exception as e:
            print(f"Exception occurred: {e}")
            flash(f"An unexpected error occurred: {e}", "danger")
            return redirect(url_for('vehicles.vehicles'))

        finally:
            cursor.close()
            close_db_connection(connection)
            print("Database connection closed")

    else:
        print("Form did not validate")
        return redirect(url_for('vehicles.vehicles'))

@add_vehicle_bp.route('/search_makes', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500

    print(f"Makes fetched: {sorted(makes)}")  # Log the fetched makes
    return jsonify(sorted(makes))

@add_vehicle_bp.route('/search_models', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500

    print(f"Models fetched for make '{make}': {sorted(models)}")  # Log the fetched models
    return jsonify(sorted(models))
