from flask import Blueprint, render_template, make_response
from app.routes.utils.utils import logout
from app.routes.utils.session import check_logged_in_redirect
from app.routes.utils.cache import disable_caching, redirect_to

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    response = check_logged_in_redirect()
    if response:
        return response
    
    redirect_to('main.index')
    response = make_response(render_template('index.html'))
    response = disable_caching(response)
    return response

@main_bp.route('/logout', methods=['POST'])
def logout_view():
    return logout()