-- Create database
CREATE DATABASE IF NOT EXISTS organ_exchange;
USE organ_exchange;

-- Hospitals table
CREATE TABLE hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    license_no VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(10) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    contact_person_name VARCHAR(255) NOT NULL,
    contact_person_phone VARCHAR(10) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_state (state)
);

-- Organ inventory table
CREATE TABLE organ_inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_id INT NOT NULL,
    organ_type ENUM('Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Eye/Cornea') NOT NULL,
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    available_units INT NOT NULL DEFAULT 0,
    status ENUM('AVAILABLE', 'NOT_AVAILABLE') DEFAULT 'AVAILABLE',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE,
    UNIQUE KEY unique_hospital_organ_blood (hospital_id, organ_type, blood_group),
    INDEX idx_search (organ_type, blood_group, status)
);

-- Requests table
CREATE TABLE requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    from_hospital_id INT NOT NULL,
    to_hospital_id INT NOT NULL,
    organ_type ENUM('Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Eye/Cornea') NOT NULL,
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    quantity_requested INT NOT NULL,
    urgency_level ENUM('HIGH', 'MEDIUM', 'LOW') NOT NULL,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'CANCELLED', 'COMPLETED') DEFAULT 'PENDING',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP NULL,
    FOREIGN KEY (from_hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE,
    FOREIGN KEY (to_hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE,
    INDEX idx_from (from_hospital_id, status),
    INDEX idx_to (to_hospital_id, status)
);

-- Sample data (optional)
INSERT INTO hospitals (name, license_no, email, phone, address, city, district, state, pincode, contact_person_name, contact_person_phone, password_hash) VALUES
('City Hospital', 'LIC001', 'city@hospital.com', '9876543210', '123 Main St', 'Mumbai', 'Mumbai City', 'Maharashtra', '400001', 'John Doe', '9876543211', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPjFpC2WzqGWi'),
('General Hospital', 'LIC002', 'general@hospital.com', '9876543212', '456 Oak Ave', 'Delhi', 'New Delhi', 'Delhi', '110001', 'Jane Smith', '9876543213', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPjFpC2WzqGWi');

-- Password for both sample hospitals: password123