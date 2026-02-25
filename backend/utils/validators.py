import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def validate_pincode(pincode):
    pattern = r'^\d{6}$'
    return re.match(pattern, pincode) is not None

def validate_password(password):
    # At least 8 characters
    return len(password) >= 8

def validate_organ_type(organ_type):
    valid_organs = ['Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Eye/Cornea']
    return organ_type in valid_organs

def validate_blood_group(blood_group):
    valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return blood_group in valid_groups

def validate_urgency(urgency):
    valid_urgencies = ['HIGH', 'MEDIUM', 'LOW']
    return urgency in valid_urgencies