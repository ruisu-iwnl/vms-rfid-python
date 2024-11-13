from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from datetime import datetime
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

    form = RFIDForm()  
    cursor, connection = get_cursor()

    try:
        cursor.execute("""
            SELECT tl.time_in, tl.time_out, u.emp_no AS employee_id, 
                CONCAT(u.firstname, ' ', u.lastname) AS name, u.contactnumber,
                GROUP_CONCAT(CONCAT(v.make, ' ', v.model) SEPARATOR ', ') AS vehicles,
                GROUP_CONCAT(v.licenseplate SEPARATOR ', ') AS license_plates,
                u.profile_image
            FROM time_logs tl
            JOIN vehicle v ON tl.vehicle_id = v.vehicle_id
            JOIN user u ON v.user_id = u.user_id
            WHERE tl.time_out IS NULL OR tl.time_out IS NOT NULL  -- includes records with empty time_out
            GROUP BY tl.time_in, tl.time_out, u.user_id
            ORDER BY 
                GREATEST(tl.time_in, COALESCE(tl.time_out, tl.time_in)) DESC
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
                'license_plates': record[6] if record[6] else 'No Plate Available',
                'profile_image': record[7]
            })

        per_page = 5
        total_records = len(structured_records)
        total_pages = (total_records + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_records = structured_records[start:end]

        return render_template('dashboard/admin/timeinout.html', records=paginated_records, page=page, total_pages=total_pages, form=form)

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
                cursor.execute("""
                    SELECT COUNT(*) FROM rfid WHERE rfid_no = %s
                """, (rfid_no,))
                exists = cursor.fetchone()[0] > 0

                if not exists:
                    flash('RFID is not registered.', 'error')
                    return redirect(url_for('timeinout.timeinout'))

                user_status = check_user_time_status(rfid_no)
                print(f"User status for RFID {rfid_no}: {user_status}")  
                
                if user_status == "No Time Logs":
                    log_time(rfid_no, 'in')  # Proceed to clock in
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in.', 'success')
                elif user_status == "Time In":
                    log_time(rfid_no, 'out')  # Proceed to clock out
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked out.', 'success')
                elif user_status == "Already Clocked Out":
                    log_time(rfid_no, 'in')  # Allow clocking in even if previously clocked out
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in.', 'success')
                    
            except Exception as e:
                print(f"An error occurred: {e}")
                flash('An error occurred while checking the RFID.', 'error')
            finally:
                cursor.close()
                close_db_connection(connection)
        else:
            flash('No RFID number scanned', 'error')
    else:
        print("Form validation failed.")  
    return redirect(url_for('timeinout.timeinout'))

def check_user_time_status(rfid_no):
    cursor, connection = get_cursor()
    try:
        cursor.execute("""
            SELECT tl.time_in, tl.time_out
            FROM time_logs tl
            JOIN rfid r ON tl.rfid_id = r.rfid_id
            WHERE r.rfid_no = %s
            ORDER BY tl.created_at DESC
            LIMIT 1
        """, (rfid_no,))
        
        result = cursor.fetchone()
        print(f"Database query result for RFID {rfid_no}: {result}")  
        
        if result is None:
            return "No Time Logs" 
        
        time_in, time_out = result
        if time_in and not time_out:
            return "Time In"
        elif time_out:
            return "Already Clocked Out"  
        else:
            return "Time In"  
    except Exception as e:
        print(f"An error occurred in check_user_time_status: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)

def log_time(rfid_no, action):
    print(f"Logging time for RFID {rfid_no} with action: {action}")
    cursor, connection = get_cursor()
    try:
        # Retrieve vehicle and user information using RFID
        cursor.execute("""
            SELECT vehicle_id FROM rfid WHERE rfid_no = %s
        """, (rfid_no,))
        vehicle_id = cursor.fetchone()

        if not vehicle_id:
            flash(f'RFID {rfid_no} is not associated with any vehicle.', 'error')
            return 

        vehicle_id = vehicle_id[0]
        now = datetime.now()

        cursor.execute("""
            SELECT user_id FROM vehicle WHERE vehicle_id = %s
        """, (vehicle_id,))
        user_id_result = cursor.fetchone()
        user_id = user_id_result[0] if user_id_result else None

        # Retrieve the latest time log status for this vehicle and RFID
        cursor.execute("""
            SELECT time_in, time_out FROM time_logs
            WHERE vehicle_id = %s AND rfid_id = (SELECT rfid_id FROM rfid WHERE rfid_no = %s)
            ORDER BY created_at DESC
            LIMIT 1
        """, (vehicle_id, rfid_no))
        latest_log = cursor.fetchone()

        if action == 'in':
            # If there's no log or the last log has a time_out (meaning it's completed), log a new "in"
            if not latest_log or latest_log[1] is not None:
                cursor.execute("""
                    INSERT INTO time_logs (vehicle_id, rfid_id, time_in)
                    VALUES (%s, (SELECT rfid_id FROM rfid WHERE rfid_no = %s), %s)
                """, (vehicle_id, rfid_no, now))
                log_login_activity(user_id, 'User', 'Clocked In')
                flash(f'Clocked in successfully for RFID: {rfid_no}', 'success')
            else:
                # If there's already an open "in" with no "out", inform the user
                flash(f'Already clocked in for RFID: {rfid_no}. Please clock out before clocking in again.', 'error')

        elif action == 'out':
            # Only log a "clock out" if there is an open "in" entry with no "out" yet
            if latest_log and latest_log[1] is None:
                cursor.execute("""
                    UPDATE time_logs
                    SET time_out = %s
                    WHERE vehicle_id = %s AND rfid_id = (SELECT rfid_id FROM rfid WHERE rfid_no = %s)
                    AND time_out IS NULL
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (now, vehicle_id, rfid_no))
                log_login_activity(user_id, 'User', 'Clocked Out')
                flash(f'Clocked out successfully for RFID: {rfid_no}', 'success')
            else:
                # If there is no open "in" entry, inform the user they need to clock in first
                flash(f'No active clock-in found for RFID: {rfid_no}. Please clock in before clocking out.', 'error')

        connection.commit()
    except Exception as e:
        print(f"An error occurred while logging time: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)
