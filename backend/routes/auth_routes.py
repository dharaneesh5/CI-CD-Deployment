from flask import Blueprint, request, jsonify, session
import bcrypt
from models import Hospital
from utils.validators import validate_email, validate_phone, validate_pincode, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'license_no', 'email', 'phone', 'address', 
                      'city', 'district', 'state', 'pincode', 'contact_person_name', 
                      'contact_person_phone', 'password']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Validate email
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate phone
    if not validate_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number (must be 10 digits)'}), 400
    
    if not validate_phone(data['contact_person_phone']):
        return jsonify({'error': 'Invalid contact person phone number'}), 400
    
    # Validate pincode
    if not validate_pincode(data['pincode']):
        return jsonify({'error': 'Invalid pincode (must be 6 digits)'}), 400
    
    # Validate password
    if not validate_password(data['password']):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Check if email already exists
    existing = Hospital.find_by_email(data['email'])
    if existing:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    try:
        hospital_id = Hospital.create(
            data['name'], data['license_no'], data['email'], data['phone'],
            data['address'], data['city'], data['district'], data['state'],
            data['pincode'], data['contact_person_name'], data['contact_person_phone'],
            password_hash
        )
        return jsonify({'message': 'Registration successful', 'hospital_id': hospital_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password required'}), 400
    
    hospital = Hospital.find_by_email(data['email'])
    
    if not hospital:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check password
    if bcrypt.checkpw(data['password'].encode('utf-8'), hospital['password_hash'].encode('utf-8')):
        session['hospital_id'] = hospital['hospital_id']
        session['hospital_name'] = hospital['name']
        return jsonify({
            'message': 'Login successful',
            'hospital': {
                'id': hospital['hospital_id'],
                'name': hospital['name'],
                'email': hospital['email']
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/session', methods=['GET'])
def check_session():
    if 'hospital_id' in session:
        return jsonify({
            'logged_in': True,
            'hospital_id': session['hospital_id'],
            'hospital_name': session.get('hospital_name', '')
        })
    return jsonify({'logged_in': False}), 401