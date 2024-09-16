from flask import Blueprint, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app.models.database import get_cursor, close_db_connection
from app.routes.utils.forms import AddUserForm
from app.routes.utils.utils import check_existing_registration
import mysql.connector

adduser_bp = Blueprint('adduser', __name__)

@adduser_bp.route('/admin/adduser', methods=['GET', 'POST'])
def add_user():
    print("Entering add_user route")
    
    admin_id = session.get('admin_id')
    if not admin_id:
        flash('Admin session not found. Please log in again.', 'error')
        print("Admin session not found, redirecting to main.index")
        return redirect(url_for('main.index'))

    form = AddUserForm()
    print("Form initialized")
    
    if form.validate_on_submit():
        print("Form validated successfully")
        
        emp_no = form.employeenumber.data
        lastname = form.lastname.data
        firstname = form.firstname.data
        email = form.email.data
        contactnumber = form.contactnumber.data
        password = form.password.data

        hashed_password = generate_password_hash(password)
        print(f"Hashed password: {hashed_password}")

        try:
            is_registered_as_user, is_registered_as_admin = check_existing_registration(email)
            print(f"Registration status: is_registered_as_user={is_registered_as_user}, is_registered_as_admin={is_registered_as_admin}")

            if is_registered_as_user:
                flash("This email is already registered as a user.", "danger")
                print("Email is already registered as a user, redirecting to userlist.userlist")
                return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))

            if is_registered_as_admin:
                flash("This email is already registered as an admin. Cannot register as a user with the same email.", "danger")
                print("Email is already registered as an admin, redirecting to userlist.userlist")
                return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))

            cursor, connection = get_cursor()
            cursor.execute("""
                INSERT INTO user (emp_no, lastname, firstname, email, contactnumber, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (emp_no, lastname, firstname, email, contactnumber, hashed_password))

            connection.commit()
            print("User added successfully")
            flash('User added successfully.', 'success')
            return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))

        except mysql.connector.IntegrityError as e:
            if e.args[0] == 1062:
                duplicate_entry_error = "An employee with this number already exists. Please use a different number."
                flash(duplicate_entry_error, 'danger')
                print(f"IntegrityError: {duplicate_entry_error}")
            else:
                flash(f"Database error: {e}", "danger")
                print(f"Database error: {e}")
            close_db_connection(connection)
            return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))

        except Exception as e:
            print(f"Exception occurred: {e}")
            flash(f"An unexpected error occurred: {e}", "danger")
            close_db_connection(connection)
            return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))

    print("Form did not validate")
    print(f"Form errors: {form.errors}")

    unique_errors = set()
    for errors in form.errors.values():
        unique_errors.update(errors)

    for error in unique_errors:
        flash(error, 'danger')
    
    return redirect(url_for('userlist.userlist', page=1, sort_by='emp_no', order='asc'))
