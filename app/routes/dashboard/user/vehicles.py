from flask import Blueprint, render_template, request, redirect, url_for, session
from app.routes.utils.session import check_access
from app.routes.utils.forms import AddVehicleForm 

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/dashboard/vehicles')

@vehicles_bp.route('/', defaults={'page': 1})
@vehicles_bp.route('/<int:page>')
def vehicles(page):
    response = check_access('user')
    if response:
        return response

    form = AddVehicleForm()

    vehicles = [
        {'car_model': 'Toyota Camry', 'car_color': 'Red', 'plate_number': 'ABC-1234'},
        {'car_model': 'Honda Accord', 'car_color': 'Blue', 'plate_number': 'XYZ-5678'},
        {'car_model': 'Ford Mustang', 'car_color': 'Black', 'plate_number': 'DEF-9012'},
        {'car_model': 'Chevrolet Malibu', 'car_color': 'White', 'plate_number': 'GHI-3456'},
        {'car_model': 'Nissan Altima', 'car_color': 'Silver', 'plate_number': 'JKL-7890'},
        {'car_model': 'Hyundai Sonata', 'car_color': 'Gray', 'plate_number': 'MNO-1234'},
        {'car_model': 'Kia Optima', 'car_color': 'Green', 'plate_number': 'PQR-5678'},
        {'car_model': 'Mazda 6', 'car_color': 'Yellow', 'plate_number': 'STU-9012'},
        {'car_model': 'Volkswagen Passat', 'car_color': 'Purple', 'plate_number': 'VWX-3456'},
        {'car_model': 'Subaru Legacy', 'car_color': 'Brown', 'plate_number': 'YZA-7890'},
        {'car_model': 'Toyota Corolla', 'car_color': 'Orange', 'plate_number': 'BCD-1234'},
        {'car_model': 'Honda Civic', 'car_color': 'Pink', 'plate_number': 'EFG-5678'},
        {'car_model': 'Ford Focus', 'car_color': 'Teal', 'plate_number': 'HIJ-9012'},
        {'car_model': 'Chevrolet Cruze', 'car_color': 'Maroon', 'plate_number': 'KLM-3456'},
        {'car_model': 'Nissan Sentra', 'car_color': 'Beige', 'plate_number': 'NOP-7890'},
        {'car_model': 'Hyundai Elantra', 'car_color': 'Cyan', 'plate_number': 'QRS-1234'},
        {'car_model': 'Kia Forte', 'car_color': 'Indigo', 'plate_number': 'TUV-5678'},
        {'car_model': 'Mazda 3', 'car_color': 'Olive', 'plate_number': 'WXY-9012'},
        {'car_model': 'Volkswagen Jetta', 'car_color': 'Lavender', 'plate_number': 'ZAB-3456'},
        {'car_model': 'Subaru Impreza', 'car_color': 'Charcoal', 'plate_number': 'CDE-7890'}
    ]

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
