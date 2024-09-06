from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..forms import UserLoginForm

user_login_bp = Blueprint('user_login', __name__)

@user_login_bp.route('', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        # Add logic to authenticate user
        return redirect(url_for('main.index'))
    return render_template('login/user_login.html', form=form)
