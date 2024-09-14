from flask import Blueprint, render_template
import traceback

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found", error_type="Not Found", traceback=None), 404

@error_bp.app_errorhandler(500)
def internal_server_error(error):
    tb = traceback.format_exc()
    return render_template('error.html', error_code=500, error_message="Internal server error", error_type="Internal Server Error", traceback=tb), 500

@error_bp.app_errorhandler(Exception)
def handle_exception(error):
    tb = traceback.format_exc()
    return render_template('error.html', error_code=500, error_message="An unexpected error occurred", error_type=type(error).__name__, traceback=tb), 500
