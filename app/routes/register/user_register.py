from flask import Blueprint, render_template, redirect, url_for, flash
from ..forms import UserRegisterForm

user_register_bp = Blueprint('user_register', __name__)

@user_register_bp.route('', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        # Add logic to register user
        return redirect(url_for('user_login.user_login'))
    return render_template('register/user_register.html', form=form)
