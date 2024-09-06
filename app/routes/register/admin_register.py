from flask import Blueprint, render_template, redirect, url_for
from ..forms import AdminRegisterForm

admin_register_bp = Blueprint('admin_register', __name__)

@admin_register_bp.route('', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        # Add logic to register admin
        return redirect(url_for('admin_login.admin_login'))
    return render_template('register/admin_register.html', form=form)
