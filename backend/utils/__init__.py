# This file makes the utils directory a Python package
# Import utility functions for easy access

from .validators import (
    validate_email,
    validate_phone,
    validate_pincode,
    validate_password,
    validate_organ_type,
    validate_blood_group,
    validate_urgency
)

# List all available utilities
__all__ = [
    'validate_email',
    'validate_phone',
    'validate_pincode',
    'validate_password',
    'validate_organ_type',
    'validate_blood_group',
    'validate_urgency'
]

# Optional: Common validation function for form data
def validate_hospital_registration_data(data):
    """Validate all hospital registration fields at once"""
    errors = []
    
    if not validate_email(data.get('email', '')):
        errors.append('Invalid email format')
    
    if not validate_phone(data.get('phone', '')):
        errors.append('Invalid phone number (must be 10 digits)')
    
    if not validate_phone(data.get('contact_person_phone', '')):
        errors.append('Invalid contact person phone number')
    
    if not validate_pincode(data.get('pincode', '')):
        errors.append('Invalid pincode (must be 6 digits)')
    
    if not validate_password(data.get('password', '')):
        errors.append('Password must be at least 8 characters')
    
    return errors

def validate_inventory_data(data):
    """Validate inventory data"""
    errors = []
    
    if not validate_organ_type(data.get('organ_type', '')):
        errors.append('Invalid organ type')
    
    if not validate_blood_group(data.get('blood_group', '')):
        errors.append('Invalid blood group')
    
    units = data.get('available_units')
    if not isinstance(units, int) or units < 0:
        errors.append('Available units must be a non-negative integer')
    
    if data.get('status') not in ['AVAILABLE', 'NOT_AVAILABLE']:
        errors.append('Status must be AVAILABLE or NOT_AVAILABLE')
    
    return errors

def validate_request_data(data):
    """Validate request data"""
    errors = []
    
    if not validate_organ_type(data.get('organ_type', '')):
        errors.append('Invalid organ type')
    
    if not validate_blood_group(data.get('blood_group', '')):
        errors.append('Invalid blood group')
    
    if not validate_urgency(data.get('urgency_level', '')):
        errors.append('Invalid urgency level')
    
    quantity = data.get('quantity_requested')
    if not isinstance(quantity, int) or quantity <= 0:
        errors.append('Quantity must be a positive integer')
    
    return errors

# Optional: Formatting utilities
def format_phone(phone):
    """Format phone number for display"""
    if not phone or len(phone) != 10:
        return phone
    return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"

def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return ''
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return ''
    # Remove any HTML tags
    import re
    return re.sub(r'<[^>]*>', '', text)