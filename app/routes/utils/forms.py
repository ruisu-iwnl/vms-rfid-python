from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Regexp
from wtforms import ValidationError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from app.models.database import get_cursor

# class AdminLoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')

# class UserLoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')
class Admin_AddUserVehicleForm(FlaskForm):
    user_id = SelectField('Select User', validators=[DataRequired()])
    make = StringField('Vehicle Make', validators=[DataRequired()])  
    model = StringField('Vehicle Model', validators=[DataRequired()])
    license_plate = StringField('License Plate', validators=[DataRequired()])
    rfid_number = StringField('RFID Number', validators=[DataRequired()])
    submit = SubmitField('Add Vehicle')

class AddVehicleForm(FlaskForm):
    car_make = StringField('Car Make', validators=[DataRequired()])
    car_model = StringField('Car Model', validators=[DataRequired()])
    plate_number = StringField('Plate Number', validators=[DataRequired()])
    rfid_number = PasswordField('RFID Number', validators=[
        DataRequired(),
        Length(min=10, max=10, message="RFID number must be exactly 10 digits."),
        Regexp('^[0-9]*$', message="RFID number must contain only digits.")
    ])


class BaseLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BaseRegisterForm(FlaskForm):
    employeenumber = StringField('Employee Number', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contactnumber = StringField('Contact Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('password_confirmation', message='Passwords must match')
    ])
    password_confirmation = PasswordField('Confirm Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    submit = SubmitField('Register')

    def validate_contactnumber(self, contactnumber):
        """
        Custom contact number validation to ensure it matches the expected format.
        """
        try:
            parsed_number = phonenumbers.parse(contactnumber.data, "PH")
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError('Invalid phone number format. Please enter a valid Philippine phone number.')
        except NumberParseException:
            raise ValidationError('Invalid phone number format. Please enter a valid Philippine phone number.')

        if len(contactnumber.data) != 11:
            raise ValidationError('Contact number must be 11 digits long.')

    def validate_password(self, password):
        """
        Custom password validator.
        """
        special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char.isupper() for char in password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char in special_characters for char in password.data):
            raise ValidationError('Password must contain at least one special character.')

    def validate_email(self, email):
        """
        Custom email validation to check for uniqueness.
        """
        cursor, connection = get_cursor()
        query = "SELECT COUNT(*) FROM {} WHERE email = %s".format(self.table_name)
        cursor.execute(query, (email.data,))
        result = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        if result > 0:
            raise ValidationError('Email address is already in use. Please use a different email.')

class UserRegisterForm(BaseRegisterForm):
    table_name = 'user'

class AdminRegisterForm(BaseRegisterForm):
    table_name = 'admin'

class AddUserForm(BaseRegisterForm):
    table_name = 'user'