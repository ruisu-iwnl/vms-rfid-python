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
            WHERE tl.time_out IS NULL OR tl.time_out IS NOT NULL
            GROUP BY tl.time_in, tl.time_out, u.user_id
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
        detected_plate_number = request.form.get('detected_plate_number', '')

        if rfid_no:
            cursor, connection = get_cursor()
            try:
                cursor.execute("""
                    SELECT rfid_id, vehicle_id FROM rfid WHERE rfid_no = %s
                """, (rfid_no,))
                rfid_data = cursor.fetchone()

                if not rfid_data:
                    flash('RFID is not registered.', 'error')
                    return redirect(url_for('timeinout.timeinout'))

                rfid_id, vehicle_id = rfid_data

                if not vehicle_id:
                    flash('RFID is registered but not associated with a vehicle.', 'error')
                    return redirect(url_for('timeinout.timeinout'))

                cleaned_detected_plate_number = detected_plate_number.replace(" ", "")
                cursor.execute("""
                    SELECT vehicle_id, licenseplate FROM vehicle WHERE REPLACE(licenseplate, ' ', '') = %s
                """, (cleaned_detected_plate_number,))
                vehicle_data = cursor.fetchone()

                if not vehicle_data:
                    flash(f"Vehicle with plate number {detected_plate_number} not found.", 'error')
                    return redirect(url_for('timeinout.timeinout'))

                detected_vehicle_id, license_plate = vehicle_data

                if vehicle_id != detected_vehicle_id:
                    flash(f"The detected plate number {detected_plate_number} is not associated with this RFID.", 'error')
                    return redirect(url_for('timeinout.timeinout'))

                user_status = check_user_time_status(rfid_no)

                if user_status == "Clock-Out Restricted":
                    flash("Cannot clock out yet. Please wait at least 30 minutes after clocking in.", "error")
                    return redirect(url_for("timeinout.timeinout"))

                if user_status == "No Time Logs":
                    log_time(rfid_no, 'in')
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in.', 'success')

                elif user_status == "Already Clocked In":
                    log_time(rfid_no, 'out')
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked out.', 'success')

                elif user_status == "Already Clocked Out":
                    log_time(rfid_no, 'in')  # Allow clocking in again after clock-out
                    flash(f'Successfully scanned RFID: {rfid_no}. User has clocked in again.', 'success')

            except Exception as e:
                flash('An error occurred while processing the RFID.', 'error')

            finally:
                cursor.close()
                close_db_connection(connection)

        else:
            flash('No RFID number scanned', 'error')

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

        if result is None:
            return "No Time Logs"

        time_in, time_out = result
        now = datetime.now()

        if time_in and not time_out:
            if now - time_in < timedelta(minutes=30):
                return "Clock-Out Restricted"
            return "Already Clocked In"

        elif time_out:
            return "Already Clocked Out"

    except Exception as e:
        return None
    finally:
        cursor.close()
        close_db_connection(connection)

def log_time(rfid_no, action):
    cursor, connection = get_cursor()
    try:
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

        cursor.execute("""
            SELECT time_in, time_out, created_at FROM time_logs
            WHERE vehicle_id = %s AND rfid_id = (SELECT rfid_id FROM rfid WHERE rfid_no = %s)
            ORDER BY created_at DESC
            LIMIT 1
        """, (vehicle_id, rfid_no))
        latest_log = cursor.fetchone()

        if action == 'in':
            if not latest_log or latest_log[1] is not None:  # No active clock-in
                cursor.execute("""
                    INSERT INTO time_logs (vehicle_id, rfid_id, time_in)
                    VALUES (%s, (SELECT rfid_id FROM rfid WHERE rfid_no = %s), %s)
                """, (vehicle_id, rfid_no, now))
                log_login_activity(user_id, 'User', 'Clocked In')
                flash(f'Clocked in successfully for RFID: {rfid_no}', 'success')
            else:
                flash(f'User with RFID {rfid_no} is already clocked in today.', 'info')

        elif action == 'out':
            if latest_log and latest_log[1] is None:  # Active clock-in
                time_in = latest_log[0]
                time_difference = now - time_in

                # If the clock-in was more than 24 hours ago, treat it as a new clock-in
                if time_difference >= timedelta(days=1):
                    # Treat as new clock-in (insert a new row)
                    cursor.execute("""
                        INSERT INTO time_logs (vehicle_id, rfid_id, time_in)
                        VALUES (%s, (SELECT rfid_id FROM rfid WHERE rfid_no = %s), %s)
                    """, (vehicle_id, rfid_no, now))
                    log_login_activity(user_id, 'User', 'Clocked In')
                    flash(f'The previous clock-in was more than 24 hours ago. Treated as new clock-in for RFID: {rfid_no}', 'success')
                elif time_difference >= timedelta(minutes=30):  # Clock-out allowed
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
                    flash(f'You cannot clock out yet. Please wait at least 30 minutes.', 'error')
            else:
                flash(f'User with RFID {rfid_no} already clocked out.', 'info')

        connection.commit()

    except Exception as e:
        flash('An error occurred while logging time.', 'error')
    finally:
        cursor.close()
        close_db_connection(connection)
