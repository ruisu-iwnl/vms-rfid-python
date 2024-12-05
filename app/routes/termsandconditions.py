from flask import Blueprint, render_template, request

tc_bp = Blueprint ('tc', __name__)

@tc_bp.route('/termsandconditions')
def tc():
    return render_template('termsandconditions.html')