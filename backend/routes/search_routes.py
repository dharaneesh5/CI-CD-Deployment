from flask import Blueprint, request, jsonify, session
from models import OrganInventory

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_organs():
    if 'hospital_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    organ_type = request.args.get('organ_type')
    blood_group = request.args.get('blood_group')
    city = request.args.get('city')
    district = request.args.get('district')
    state = request.args.get('state')
    
    # Validate organ type if provided
    if organ_type:
        valid_organs = ['Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Eye/Cornea']
        if organ_type not in valid_organs:
            return jsonify({'error': 'Invalid organ type'}), 400
    
    # Validate blood group if provided
    if blood_group:
        valid_blood = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_group not in valid_blood:
            return jsonify({'error': 'Invalid blood group'}), 400
    
    try:
        results = OrganInventory.search_available(organ_type, blood_group, city, district, state)
        
        # Remove contact details from results
        for result in results:
            result.pop('email', None)
            result.pop('phone', None)
            result.pop('contact_person_name', None)
            result.pop('contact_person_phone', None)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500