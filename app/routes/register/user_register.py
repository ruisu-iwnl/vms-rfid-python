from flask import Blueprint, render_template, redirect, url_for, flash
from ..forms import UserRegisterForm
from app.models.database import get_cursor, close_db_connection
from ..utils import hash_password

user_register_bp = Blueprint('user_register', __name__)

@user_register_bp.route('', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        try:
            # print("Form validated successfully.")

            cursor, connection = get_cursor()
            # print("Database cursor and connection established.")

            hashed_password = hash_password(form.password.data)
            # print(f"Hashed password: {hashed_password}")

            query = """
                INSERT INTO user (emp_no, lastname, firstname, email, contactnumber, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                form.employeenumber.data,
                form.lastname.data,
                form.firstname.data,
                form.email.data,
                form.contactnumber.data,
                hashed_password
            )
            # print(f"Executing query: {query} with values {values}")

            cursor.execute(query, values)
            connection.commit()
            print("Data committed to the database.")

            cursor.close()
            close_db_connection(connection)

            #hindi pa gumagana to sa user_dashboard
            flash("Registration successful", "success")
            return redirect(url_for('user_dashboard.user_dashboard'))

        except Exception as e:
            print(f"Exception occurred: {e}")
            flash(f"Error: {e}", "whats up danger")
            return redirect(url_for('user_register.user_register'))

    return render_template('register/user_register.html', form=form)
