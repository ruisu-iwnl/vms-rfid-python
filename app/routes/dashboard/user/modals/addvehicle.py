from flask import Blueprint, redirect, flash, request, url_for, session
from app.routes.utils.forms import AddVehicleForm
import mysql.connector
from app.models.database import get_cursor, close_db_connection
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
    print(f"check_access response: {response}")

    if response:
        print("Unauthorized access detected, redirecting...")
        return response

    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")
    
    if not user_id:
        print("User ID is not set in the session. User might not be logged in.")
        flash("You need to be logged in to add a vehicle.", "danger")
        return redirect(url_for('main.index'))
    
    form = AddVehicleForm()

    if form.validate_on_submit():
        print("Form validated successfully")
        car_model = form.car_model.data
        plate_number = form.plate_number.data
        rfid_number = form.rfid_number.data

        print(f"Form data - Car Model: {car_model}, Plate Number: {plate_number}, RFID Number: {rfid_number}")

        try:
            cursor, connection = get_cursor()
            print("Database connection established")

            # Check if the RFID number is registered
            if rfid_number and not is_rfid_valid(rfid_number):
                flash("The provided RFID number is not registered.", "danger")
                return redirect(url_for('vehicles.vehicles'))

            # Check for duplicate license plate
            cursor.execute("SELECT vehicle_id FROM vehicle WHERE licenseplate = %s", (plate_number,))
            existing_vehicle = cursor.fetchone()
            print(f"Existing vehicle check result: {existing_vehicle}")

            if existing_vehicle:
                flash("This license plate is already registered.", "danger")
                return redirect(url_for('vehicles.vehicles'))

            # Add vehicle to the database
            cursor.execute("INSERT INTO vehicle (user_id, licenseplate, model) VALUES (%s, %s, %s)",
                           (user_id, plate_number, car_model))
            vehicle_id = cursor.lastrowid
            print(f"Inserted vehicle ID: {vehicle_id}")

            # Associate RFID with the vehicle
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
            details = f"Added vehicle with Model: {car_model} \n RFID Number: {rfid_number}"
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
