from flask import Blueprint, request, jsonify, session
from models import OrganInventory

inventory_bp = Blueprint('inventory', __name__)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'hospital_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@inventory_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    hospital_id = session['hospital_id']
    inventory = OrganInventory.get_hospital_inventory(hospital_id)
    return jsonify(inventory), 200

@inventory_bp.route('/inventory/add', methods=['POST'])
@login_required
def add_inventory():
    hospital_id = session['hospital_id']
    data = request.json
    
    required_fields = ['organ_type', 'blood_group', 'available_units', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Validate organ type
    valid_organs = ['Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Eye/Cornea']
    if data['organ_type'] not in valid_organs:
        return jsonify({'error': 'Invalid organ type'}), 400
    
    # Validate blood group
    valid_blood = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if data['blood_group'] not in valid_blood:
        return jsonify({'error': 'Invalid blood group'}), 400
    
    # Validate units
    if not isinstance(data['available_units'], int) or data['available_units'] < 0:
        return jsonify({'error': 'Available units must be a non-negative integer'}), 400
    
    # Validate status
    if data['status'] not in ['AVAILABLE', 'NOT_AVAILABLE']:
        return jsonify({'error': 'Status must be AVAILABLE or NOT_AVAILABLE'}), 400
    
    try:
        OrganInventory.add_or_update(
            hospital_id,
            data['organ_type'],
            data['blood_group'],
            data['available_units'],
            data['status']
        )
        return jsonify({'message': 'Inventory updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/inventory/update', methods=['POST'])
@login_required
def update_inventory():
    # Same as add, since we use add_or_update method
    return add_inventory()