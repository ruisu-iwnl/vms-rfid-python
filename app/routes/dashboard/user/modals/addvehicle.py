from flask import Blueprint, render_template, redirect, flash, request, url_for, session
from app.routes.utils.forms import AddVehicleForm
import mysql.connector
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.session import check_access

add_vehicle_bp = Blueprint('add_vehicle', __name__, url_prefix='/add_vehicle')

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

        duplicate_entry_error = None
        database_error = None

        try:
            cursor, connection = get_cursor()
            print("Database connection established")

            cursor.execute("SELECT vehicle_id FROM vehicle WHERE licenseplate = %s", (plate_number,))
            existing_vehicle = cursor.fetchone()
            print(f"Existing vehicle check result: {existing_vehicle}")

            if existing_vehicle:
                duplicate_entry_error = "This license plate is already registered."
                print(duplicate_entry_error)
                flash(duplicate_entry_error, "danger")
                return redirect(url_for('vehicles.vehicles'))

            query = """
                INSERT INTO vehicle (user_id, licenseplate, model)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, plate_number, car_model))
            vehicle_id = cursor.lastrowid
            print(f"Inserted vehicle ID: {vehicle_id}")

            cursor.execute("INSERT INTO rfid (rfid_no, vehicle_id) VALUES (%s, %s)", (rfid_number, vehicle_id))
            print(f"Inserted RFID number: {rfid_number}")

            connection.commit()
            flash("Vehicle added successfully", "success")
            print("Vehicle added successfully, redirecting...")

            return redirect(url_for('vehicles.vehicles'))

        except mysql.connector.IntegrityError as e:
            print(f"Database integrity error: {e}")
            if e.args[0] == 1062:
                duplicate_entry_error = "An RFID number is already associated with another vehicle. Please use a different RFID number."
                flash(duplicate_entry_error, "danger")
            else:
                database_error = f"Database error: {e}"
                flash(database_error, "danger")
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
