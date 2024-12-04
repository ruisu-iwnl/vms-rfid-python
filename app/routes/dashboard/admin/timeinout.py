from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from app.routes.utils.activity_log import log_login_activity

class RFIDForm(FlaskForm):
    rfid_no = StringField('RFID Scanner', validators=[DataRequired()])
    submit = SubmitField('Submit')

timeinout_bp = Blueprint('timeinout', __name__, url_prefix='/dashboard/timeinout')

@timeinout_bp.route('/', defaults={'page': 1})
@timeinout_bp.route('/<int:page>')
def timeinout(page):
    response = check_access('admin')
    if response:
        return response

    # Check if user is a super admin
    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        print("This admin is a super admin.")
        super_admin_features = True
    else:
        print("This admin is NOT a super admin.")
        super_admin_features = False

    form = RFIDForm()  
    cursor, connection = get_cursor()

    try:
        # Updated query to fetch admin's first name
        cursor.execute("""
            SELECT tl.time_in, tl.time_out, u.emp_no AS employee_id, 
                CONCAT(u.firstname, ' ', u.lastname) AS name, u.contactnumber,
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                u.profile_image, a.firstname AS admin_firstname  -- Changed to fetch admin's first name
            FROM time_logs tl
            JOIN vehicle v ON tl.vehicle_id = v.vehicle_id
            JOIN user u ON v.user_id = u.user_id
            LEFT JOIN admin a ON tl.admin_id = a.admin_id  -- Join to get the admin's first name
            WHERE tl.time_out IS NULL OR tl.time_out IS NOT NULL
            GROUP BY tl.time_in, tl.time_out, u.user_id, tl.admin_id
            ORDER BY GREATEST(tl.time_in, COALESCE(tl.time_out, tl.time_in)) DESC
        """)

        records = cursor.fetchall()

        structured_records = []
        for record in records:
            structured_records.append({
                'date': record[0].date(),
                'time_in': record[0].time(),
                'time_out': record[1].time() if record[1] else None,
                'employee_id': record[2],
                'name': record[3],
                'phone_number': record[4],
                'vehicles': record[5] if record[5] else 'No Vehicle Registered',
                'profile_image': record[6],
                'admin_firstname': record[7]  # Changed to admin_firstname
            })

        per_page = 5
        total_records = len(structured_records)
        total_pages = (total_records + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_records = structured_records[start:end]

        return render_template('dashboard/admin/timeinout.html', records=paginated_records, page=page, total_pages=total_pages, form=form, super_admin_features=super_admin_features)

    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for('timeinout.timeinout'))

    finally:
        cursor.close()
        close_db_connection(connection)

@timeinout_bp.route('/time_logs/rfid', methods=['POST'])
def handle_rfid():
    form = RFIDForm()
    if form.validate_on_submit():
        rfid_no = form.rfid_no.data
        print(f"RFID scanned: {rfid_no}")

        if rfid_no:
            cursor, connection = get_cursor()
            try:
                print("Querying RFID data...")

                # Query the RFID table for the provided RFID number
                cursor.execute("""
                    SELECT r.rfid_id, v.vehicle_id, v.user_id
                    FROM rfid r
                    JOIN vehicle v ON r.rfid_no = v.rfid_no
                    WHERE r.rfid_no = %s
                """, (rfid_no,))
                rfid_data = cursor.fetchone()
                print(f"RFID data fetched: {rfid_data}")

                if not rfid_data:
                    print(f"RFID {rfid_no} is not registered or not associated with a vehicle.")
                    flash('RFID is not registered or not associated with a vehicle.', 'error')
                    return redirect(url_for('timeinout.timeinout'))

                rfid_id, vehicle_id, user_id = rfid_data
                print(f"RFID ID: {rfid_id}, Vehicle ID: {vehicle_id}, User ID: {user_id}")

                # Check if the vehicle is assigned to a user
                if not vehicle_id:
                    print("RFID is registered but not associated with a vehicle.")
                    flash('RFID is registered but not associated with a vehicle.', 'error')
                    return redirect(url_for('timeinout.timeinout'))

                user_status = check_user_time_status(rfid_no)
                print(f"User status: {user_status}")

                if user_status == "Clock-Out Restricted":
                    print("Cannot clock out yet. Waiting period not met.")
                    flash("Cannot clock out yet. Please wait at least 30 minutes after clocking in.", "error")
                    return redirect(url_for("timeinout.timeinout"))

                if user_status == "Clock-In Restricted":
                    print("Cannot clock in yet. Waiting period not met.")
                    flash("Cannot clock in yet. Please wait at least 30 minutes after clocking out.", "error")
                    return redirect(url_for("timeinout.timeinout"))

                if user_status == "No Time Logs":
                    print(f"Logging clock-in for RFID: {rfid_no}")
                    log_time(rfid_no, 'in', vehicle_id, rfid_id, user_id)
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in.', 'success')

                elif user_status == "Already Clocked In":
                    print(f"Logging clock-out for RFID: {rfid_no}")
                    log_time(rfid_no, 'out', vehicle_id, rfid_id, user_id)
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked out.', 'success')

                elif user_status == "Already Clocked Out":
                    print(f"Logging clock-in again for RFID: {rfid_no}")
                    log_time(rfid_no, 'in', vehicle_id, rfid_id, user_id)
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in again.', 'success')

            except Exception as e:
                print(f"Error occurred: {e}")
                flash('An error occurred while processing the RFID.', 'error')

            finally:
                cursor.close()
                close_db_connection(connection)

        else:
            print("No RFID number scanned.")
            flash('No RFID number scanned', 'error')

    return redirect(url_for('timeinout.timeinout'))

def check_user_time_status(rfid_no):
    cursor, connection = get_cursor()
    try:
        print(f"Checking time status for RFID: {rfid_no}")

        # Fetch the most recent time log entry for the given RFID number
        cursor.execute("""
            SELECT tl.time_in, tl.time_out
            FROM time_logs tl
            JOIN rfid r ON tl.rfid_id = r.rfid_id
            WHERE r.rfid_no = %s
            ORDER BY tl.created_at DESC
            LIMIT 1
        """, (rfid_no,))

        result = cursor.fetchone()
        print(f"Fetched result: {result}")

        if result is None:
            print("No time logs found for RFID.")
            return "No Time Logs"

        time_in, time_out = result
        now = datetime.now()
        print(f"Time In: {time_in}, Time Out: {time_out} | Current Time: {now}")

        # If user is clocked in but hasn't clocked out yet
        if time_in and not time_out:
            print(f"User is clocked in, but hasn't clocked out.")
            if now - time_in < timedelta(minutes=30):
                print("Clock-out restricted. Less than 30 minutes passed since clock-in.")
                return "Clock-Out Restricted"
            print("User is already clocked in.")
            return "Already Clocked In"

        # If user has clocked out, check if they can clock in again
        if time_out:
            print(f"User has clocked out. Checking if they can clock in again.")
            if now - time_out < timedelta(minutes=30):
                print("Clock-in restricted. Less than 30 minutes passed since clock-out.")
                return "Clock-In Restricted"
            print("User can clock in again.")
            return "Already Clocked Out"

    except Exception as e:
        print(f"Error occurred while checking time status: {e}")
        return None
    finally:
        print("Closing cursor and connection.")
        cursor.close()
        close_db_connection(connection)

from flask import session

def log_time(rfid_no, action, vehicle_id, rfid_id, user_id):
    cursor, connection = get_cursor()
    try:
        now = datetime.now()
        print(f"Logging time for RFID: {rfid_no} | Action: {action} | Vehicle ID: {vehicle_id} | RFID ID: {rfid_id} | User ID: {user_id}")

        # Fetch admin_id from session, use fallback value (admin_id = 16) if not present
        admin_id = session.get('admin_id')
        if not admin_id:
            # If no admin_id in session, fetch the admin_id 16 from the database
            print("No admin_id in session, fetching admin_id = 16 from database.")
            cursor.execute("SELECT admin_id FROM admin WHERE admin_id = %s", (16,))
            admin_result = cursor.fetchone()
            if admin_result:
                admin_id = admin_result[0]
            else:
                # If admin_id 16 does not exist, use "Guest" for debugging purposes
                print("Admin ID 16 not found, using 'Guest' for admin_id.")
                admin_id = 'Guest'
        print(f"Using admin_id: {admin_id}")

        # Fetch the latest time log for the vehicle and RFID
        cursor.execute("""
            SELECT time_in, time_out, created_at FROM time_logs
            WHERE vehicle_id = %s AND rfid_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (vehicle_id, rfid_id))
        latest_log = cursor.fetchone()
        print(f"Latest log fetched: {latest_log}")

        if action == 'in':
            print("Processing clock-in...")
            if not latest_log or latest_log[1] is not None:  # No active clock-in
                print(f"Performing clock-in for RFID {rfid_no} at {now}")
                cursor.execute("""
                    INSERT INTO time_logs (vehicle_id, rfid_id, time_in, admin_id)
                    VALUES (%s, %s, %s, %s)
                """, (vehicle_id, rfid_id, now, admin_id))  # Use fetched admin_id
                log_login_activity(user_id, 'User', 'Clocked In')
                flash(f'Clocked in successfully for RFID: {rfid_no}', 'success')
            else:
                print(f"User with RFID {rfid_no} is already clocked in today.")
                flash(f'User with RFID {rfid_no} is already clocked in today.', 'info')

        elif action == 'out':
            print("Processing clock-out...")
            if latest_log and latest_log[1] is None:  # Active clock-in
                time_in = latest_log[0]
                time_difference = now - time_in
                print(f"Time difference: {time_difference} | Clock-out allowed?")

                # If the clock-in was more than 24 hours ago, treat it as a new clock-in
                if time_difference >= timedelta(days=1):
                    print(f"Clock-in more than 24 hours ago. Treating as new clock-in.")
                    cursor.execute("""
                        INSERT INTO time_logs (vehicle_id, rfid_id, time_in, admin_id)
                        VALUES (%s, %s, %s, %s)
                    """, (vehicle_id, rfid_id, now, admin_id))  # Use fetched admin_id
                    log_login_activity(user_id, 'User', 'Clocked In')
                    flash(f'The previous clock-in was more than 24 hours ago. Treated as new clock-in for RFID: {rfid_no}', 'success')
                elif time_difference >= timedelta(minutes=30):  # Clock-out allowed
                    print(f"Clock-out allowed. Updating time_out for RFID {rfid_no}")
                    cursor.execute("""
                        UPDATE time_logs
                        SET time_out = %s
                        WHERE vehicle_id = %s AND rfid_id = %s
                        AND time_out IS NULL
                        ORDER BY created_at DESC
                        LIMIT 1
                    """, (now, vehicle_id, rfid_id))
                    log_login_activity(user_id, 'User', 'Clocked Out')
                    flash(f'Clocked out successfully for RFID: {rfid_no}', 'success')
                else:
                    print(f"Clock-out not allowed. Please wait at least 30 minutes.")
                    flash(f'You cannot clock out yet. Please wait at least 30 minutes.', 'error')
            else:
                print(f"User with RFID {rfid_no} already clocked out.")
                flash(f'User with RFID {rfid_no} already clocked out.', 'info')

        connection.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
        flash('An error occurred while logging time.', 'error')
    finally:
        print("Closing cursor and connection.")
        cursor.close()
        close_db_connection(connection)
