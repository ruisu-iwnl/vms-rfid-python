from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..forms import AdminLoginForm

admin_login_bp = Blueprint('admin_login', __name__)

@admin_login_bp.route('', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Add logic to authenticate admin
        return redirect(url_for('main.index'))
    return render_template('login/admin_login.html', form=form)
