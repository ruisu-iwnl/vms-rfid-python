from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.models.database import get_db_connection, close_db_connection
from app.routes.utils.session import check_access
import mysql.connector

class RFIDForm(FlaskForm):
    rfid_no = StringField('Enter RFID', render_kw={"placeholder": "RFID Number"}, validators=[DataRequired()])
    submit = SubmitField('Submit')

rfid_bp = Blueprint('rfid', __name__)

@rfid_bp.route('', methods=['GET', 'POST'])
def add_rfid():
    response = check_access('admin')
    if response:
        return response
    
    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        print("This admin is a super admin.")

        super_admin_features = True
    else:
        print("This admin is NOT a super admin.")
        super_admin_features = False


    form = RFIDForm()

    if form.validate_on_submit():
        rfid_no = form.rfid_no.data
        
        if rfid_no.isdigit() and len(rfid_no) == 10:
            print(f"Adding RFID: {rfid_no}")
            success = add_rfid_to_db(rfid_no)

            if success:
                flash("RFID added successfully!", "success")
                return redirect(url_for('rfid.add_rfid'))
            else:
                print("Failed to add RFID.")
        else:
            flash("Invalid RFID number. Please enter a 10-digit number.", "danger")

    print("Form did not validate.")
    print(f"Form errors: {form.errors}")

    # Set default pagination values
    page = 1  # You can change this based on user navigation
    sort_by = 'rfid_id'
    order = 'asc'

    rfid_records = fetch_rfids() 
    per_page = 5
    total_pages = (len(rfid_records) + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    paginated_records = rfid_records[start:start + per_page]

    return render_template(
        'dashboard/admin/rfid.html',
        form=form,
        records=paginated_records,  
        page=page,
        total_pages=total_pages,
        sort_by=sort_by,
        order=order,
        super_admin_features=super_admin_features
    )

@rfid_bp.route('/list', defaults={'page': 1, 'sort_by': 'rfid_id', 'order': 'asc'})
@rfid_bp.route('/list/<int:page>/<string:sort_by>/<string:order>')
def list_rfid(page, sort_by='rfid_id', order='asc'):
    response = check_access('admin')
    if response:
        return response
    
    is_super_admin = session.get('is_super_admin', False)
    if is_super_admin:
        print("This admin is a super admin.")

        super_admin_features = True
    else:
        print("This admin is NOT a super admin.")
        super_admin_features = False

    valid_columns = {'rfid_id': 'rfid_id', 'rfid_no': 'rfid_no', 'vehicle_id': 'vehicle_id', 'created_at': 'created_at'}
    
    sort_column = valid_columns.get(sort_by, 'rfid_id')
    sort_order = 'ASC' if order == 'asc' else 'DESC'
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get RFID entries with sorting
    query = f"""
        SELECT rfid_id, rfid_no, vehicle_id, created_at
        FROM rfid
        ORDER BY {sort_column} {sort_order}
        LIMIT %s OFFSET %s;
    """
    
    per_page = 5
    offset = (page - 1) * per_page

    cursor.execute(query, (per_page, offset))
    records = cursor.fetchall()

    # Count total records for pagination
    count_query = "SELECT COUNT(*) FROM rfid;"
    cursor.execute(count_query)
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + per_page - 1) // per_page

    cursor.close()
    close_db_connection(conn)

    form = RFIDForm()  

    return render_template('dashboard/admin/rfid.html', records=records, page=page, total_pages=total_pages, sort_by=sort_by, order=order, form=form, super_admin_features=super_admin_features)

def fetch_rfids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rfid_id, rfid_no, vehicle_id, created_at FROM rfid")
    records = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)
    return records

def add_rfid_to_db(rfid_no):
    print(f"Adding RFID to database: rfid_no={rfid_no}")
    conn = get_db_connection()
    cursor = conn.cursor()
    success = False

    try:
        cursor.execute("INSERT INTO rfid (rfid_no) VALUES (%s)", (rfid_no,))
        conn.commit()
        print("RFID data successfully added.")
        success = True
    except mysql.connector.IntegrityError as e:
        if e.errno == 1062:  
            flash("This RFID number is already registered.", "danger")
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
