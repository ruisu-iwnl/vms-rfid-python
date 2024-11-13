from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.utils.session import check_access
from app.routes.utils.forms import AddVehicleForm
from app.models.database import get_cursor, close_db_connection

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/dashboard/vehicles')

@vehicles_bp.route('/', defaults={'page': 1})
@vehicles_bp.route('/<int:page>')
def vehicles(page):
    response = check_access('user')
    if response:
        return response

    form = AddVehicleForm()

    user_id = session.get('user_id')

    cursor, connection = get_cursor()

    try:
        cursor.execute("""
            SELECT v.make, v.model, v.licenseplate, v.created_at, r.rfid_no
            FROM vehicle v
            LEFT JOIN rfid r ON v.vehicle_id = r.vehicle_id
            WHERE v.user_id = %s
        """, (user_id,))
        
        vehicles = cursor.fetchall()  

    finally:
        close_db_connection(connection)

    per_page = 5
    total_vehicles = len(vehicles)
    total_pages = (total_vehicles + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_vehicles = vehicles[start:end]

    return render_template(
        'dashboard/user/vehicles.html',
        vehicles=paginated_vehicles,
        page=page,
        total_pages=total_pages,
        form=form
    )
