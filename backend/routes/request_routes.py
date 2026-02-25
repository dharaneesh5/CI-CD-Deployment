from flask import Blueprint, request, jsonify, session
from models import Request, OrganInventory
from utils.validators import validate_organ_type, validate_blood_group, validate_urgency

request_bp = Blueprint('requests', __name__)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'hospital_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@request_bp.route('/request/create', methods=['POST'])
@login_required
def create_request():
    from_hospital_id = session['hospital_id']
    data = request.json
    
    required_fields = ['to_hospital_id', 'organ_type', 'blood_group', 'quantity_requested', 'urgency_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Validate organ type
    if not validate_organ_type(data['organ_type']):
        return jsonify({'error': 'Invalid organ type'}), 400
    
    # Validate blood group
    if not validate_blood_group(data['blood_group']):
        return jsonify({'error': 'Invalid blood group'}), 400
    
    # Validate urgency
    if not validate_urgency(data['urgency_level']):
        return jsonify({'error': 'Invalid urgency level'}), 400
    
    # Validate quantity
    if not isinstance(data['quantity_requested'], int) or data['quantity_requested'] <= 0:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400
    
    # Check if trying to request from self
    if from_hospital_id == data['to_hospital_id']:
        return jsonify({'error': 'Cannot request organs from your own hospital'}), 400
    
    # Check if the target hospital has enough stock
    try:
        inventory = OrganInventory.get_by_hospital_and_type(
            data['to_hospital_id'],
            data['organ_type'],
            data['blood_group']
        )
        
        if not inventory or inventory['available_units'] < data['quantity_requested']:
            return jsonify({'error': 'Requested quantity not available'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error checking inventory: {str(e)}'}), 500
    
    try:
        request_id = Request.create(
            from_hospital_id,
            data['to_hospital_id'],
            data['organ_type'],
            data['blood_group'],
            data['quantity_requested'],
            data['urgency_level']
        )
        return jsonify({'message': 'Request created successfully', 'request_id': request_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/request/incoming', methods=['GET'])
@login_required
def get_incoming_requests():
    hospital_id = session['hospital_id']
    
    try:
        requests = Request.get_incoming(hospital_id)
        
        # Hide contact details for pending/rejected requests
        for req in requests:
            if req['status'] != 'ACCEPTED':
                # Remove contact details for non-accepted requests
                req.pop('phone', None)
                req.pop('email', None)
                req.pop('contact_person_name', None)
                req.pop('contact_person_phone', None)
        
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/request/outgoing', methods=['GET'])
@login_required
def get_outgoing_requests():
    hospital_id = session['hospital_id']
    
    try:
        requests = Request.get_outgoing(hospital_id)
        
        # Only show contact details if request is accepted
        for req in requests:
            if req['status'] != 'ACCEPTED':
                req.pop('phone', None)
                req.pop('email', None)
                req.pop('contact_person_name', None)
                req.pop('contact_person_phone', None)
        
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/request/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    hospital_id = session['hospital_id']
    
    try:
        success = Request.accept_request(request_id, hospital_id)
        if success:
            return jsonify({'message': 'Request accepted successfully'}), 200
        else:
            return jsonify({'error': 'Unable to accept request. Insufficient stock or request not found.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/request/reject/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    hospital_id = session['hospital_id']
    
    try:
        success = Request.reject_request(request_id, hospital_id)
        if success:
            return jsonify({'message': 'Request rejected successfully'}), 200
        else:
            return jsonify({'error': 'Request not found or already processed'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/request/complete/<int:request_id>', methods=['POST'])
@login_required
def complete_request(request_id):
    hospital_id = session['hospital_id']
    
    try:
        success = Request.complete_request(request_id, hospital_id)
        if success:
            return jsonify({'message': 'Request completed successfully'}), 200
        else:
            return jsonify({'error': 'Unable to complete request. Request may not be in ACCEPTED state.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optional: Add endpoint to cancel a request
@request_bp.route('/request/cancel/<int:request_id>', methods=['POST'])
@login_required
def cancel_request(request_id):
    hospital_id = session['hospital_id']
    
    try:
        success = Request.cancel_request(request_id, hospital_id)
        if success:
            return jsonify({'message': 'Request cancelled successfully'}), 200
        else:
            return jsonify({'error': 'Unable to cancel request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500