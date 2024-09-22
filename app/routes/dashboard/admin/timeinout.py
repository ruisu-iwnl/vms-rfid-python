from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.routes.utils.session import check_access
from app.models.database import get_cursor, close_db_connection
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

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
            SELECT tl.time_in, tl.time_out, v.user_id, u.firstname, u.lastname, u.contactnumber
            FROM time_logs tl
            JOIN vehicle v ON tl.vehicle_id = v.vehicle_id
            JOIN user u ON v.user_id = u.user_id
            ORDER BY tl.created_at DESC
        """)
        
        records = cursor.fetchall()

        structured_records = []
        for record in records:
            structured_records.append({
                'date': record[0].date(),
                'time_in': record[0].time(),
                'time_out': record[1].time() if record[1] else None,
                'employee_id': record[2],
                'name': f"{record[3]} {record[4]}",
                'phone_number': record[5]
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
        if rfid_no:
            flash(f'Successfully scanned RFID: {rfid_no}', 'success')
        else:
            flash('No RFID number scanned', 'error')
    return redirect(url_for('timeinout.timeinout'))
