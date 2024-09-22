import mysql.connector
from app.models.database import get_db_connection, close_db_connection
from flask import render_template, jsonify,flash,request

def add_vehicle_to_db(user_id, make, model, license_plate, rfid_number):
    print(f"Adding vehicle to database: user_id={user_id}, make={make}, model={model}, license_plate={license_plate}, rfid_number={rfid_number}")
    conn = get_db_connection()
    cursor = conn.cursor()
    success = False

    try:
        if rfid_number:
            cursor.execute('SELECT vehicle_id FROM rfid WHERE rfid_no = %s', (rfid_number,))
            existing_rfid = cursor.fetchone()

            if existing_rfid is None:
                flash("The provided RFID number is not registered.", "danger")
                return False
            
            if existing_rfid[0] is not None:
                flash("This RFID number is already registered to a vehicle.", "danger")
                return False
        
        cursor.execute('INSERT INTO vehicle (user_id, make, model, licenseplate) VALUES (%s, %s, %s, %s)', 
                       (user_id, make, model, license_plate))
        vehicle_id = cursor.lastrowid

        if rfid_number:
            cursor.execute('UPDATE rfid SET vehicle_id = %s WHERE rfid_no = %s', 
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


def get_users():
    print("Fetching users from the database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, firstname FROM user') 
    users = cursor.fetchall()
    close_db_connection(conn)
    print(f"Users fetched: {users}")
    return users

def is_rfid_valid(rfid_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM rfid WHERE rfid_no = %s', (rfid_number,))
    count = cursor.fetchone()[0]
    close_db_connection(conn)
    return count > 0
