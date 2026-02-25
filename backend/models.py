import mysql.connector
from db_config import get_db_connection
from datetime import datetime

class Hospital:
    @staticmethod
    def create(name, license_no, email, phone, address, city, district, state, 
               pincode, contact_person_name, contact_person_phone, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO hospitals (name, license_no, email, phone, address, city, 
                              district, state, pincode, contact_person_name, 
                              contact_person_phone, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, license_no, email, phone, address, city, district, 
                 state, pincode, contact_person_name, contact_person_phone, password_hash)
        cursor.execute(query, values)
        conn.commit()
        hospital_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return hospital_id

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM hospitals WHERE email = %s"
        cursor.execute(query, (email,))
        hospital = cursor.fetchone()
        cursor.close()
        conn.close()
        return hospital

    @staticmethod
    def find_by_id(hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM hospitals WHERE hospital_id = %s"
        cursor.execute(query, (hospital_id,))
        hospital = cursor.fetchone()
        cursor.close()
        conn.close()
        return hospital

    @staticmethod
    def get_all_hospitals():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT hospital_id, name, city, district, state FROM hospitals"
        cursor.execute(query)
        hospitals = cursor.fetchall()
        cursor.close()
        conn.close()
        return hospitals


class OrganInventory:
    @staticmethod
    def add_or_update(hospital_id, organ_type, blood_group, available_units, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if record exists
        check_query = """
        SELECT inventory_id FROM organ_inventory 
        WHERE hospital_id = %s AND organ_type = %s AND blood_group = %s
        """
        cursor.execute(check_query, (hospital_id, organ_type, blood_group))
        existing = cursor.fetchone()
        
        if existing:
            # Update
            query = """
            UPDATE organ_inventory 
            SET available_units = %s, status = %s, last_updated = NOW()
            WHERE hospital_id = %s AND organ_type = %s AND blood_group = %s
            """
            cursor.execute(query, (available_units, status, hospital_id, organ_type, blood_group))
        else:
            # Insert
            query = """
            INSERT INTO organ_inventory (hospital_id, organ_type, blood_group, available_units, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (hospital_id, organ_type, blood_group, available_units, status))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_hospital_inventory(hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM organ_inventory WHERE hospital_id = %s ORDER BY organ_type, blood_group"
        cursor.execute(query, (hospital_id,))
        inventory = cursor.fetchall()
        cursor.close()
        conn.close()
        return inventory

    @staticmethod
    def search_available(organ_type=None, blood_group=None, city=None, district=None, state=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT oi.*, h.name, h.city, h.district, h.state, h.address, 
               h.phone, h.email, h.contact_person_name, h.contact_person_phone
        FROM organ_inventory oi
        JOIN hospitals h ON oi.hospital_id = h.hospital_id
        WHERE oi.available_units > 0 AND oi.status = 'AVAILABLE'
        """
        params = []
        
        if organ_type:
            query += " AND oi.organ_type = %s"
            params.append(organ_type)
        
        if blood_group:
            query += " AND oi.blood_group = %s"
            params.append(blood_group)
        
        if city:
            query += " AND h.city LIKE %s"
            params.append(f"%{city}%")
        
        if district:
            query += " AND h.district LIKE %s"
            params.append(f"%{district}%")
        
        if state:
            query += " AND h.state LIKE %s"
            params.append(f"%{state}%")
        
        query += " ORDER BY h.name, oi.organ_type"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_by_hospital_and_type(hospital_id, organ_type, blood_group):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT * FROM organ_inventory 
        WHERE hospital_id = %s AND organ_type = %s AND blood_group = %s
        """
        cursor.execute(query, (hospital_id, organ_type, blood_group))
        inventory = cursor.fetchone()
        cursor.close()
        conn.close()
        return inventory


class Request:
    @staticmethod
    def create(from_hospital_id, to_hospital_id, organ_type, blood_group, 
               quantity_requested, urgency_level):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO requests (from_hospital_id, to_hospital_id, organ_type, 
                             blood_group, quantity_requested, urgency_level, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'PENDING')
        """
        values = (from_hospital_id, to_hospital_id, organ_type, blood_group, 
                 quantity_requested, urgency_level)
        cursor.execute(query, values)
        conn.commit()
        request_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return request_id

    @staticmethod
    def get_incoming(hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT r.*, h.name as from_hospital_name, h.city, h.state, 
               h.phone, h.email, h.contact_person_name, h.contact_person_phone
        FROM requests r
        JOIN hospitals h ON r.from_hospital_id = h.hospital_id
        WHERE r.to_hospital_id = %s
        ORDER BY r.requested_at DESC
        """
        cursor.execute(query, (hospital_id,))
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests

    @staticmethod
    def get_outgoing(hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT r.*, h.name as to_hospital_name, h.city, h.state, h.address,
               h.phone, h.email, h.contact_person_name, h.contact_person_phone
        FROM requests r
        JOIN hospitals h ON r.to_hospital_id = h.hospital_id
        WHERE r.from_hospital_id = %s
        ORDER BY r.requested_at DESC
        """
        cursor.execute(query, (hospital_id,))
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests

    @staticmethod
    def get_by_id(request_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM requests WHERE request_id = %s"
        cursor.execute(query, (request_id,))
        request = cursor.fetchone()
        cursor.close()
        conn.close()
        return request

    @staticmethod
    def accept_request(request_id, hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Start transaction
            conn.start_transaction()
            
            # Get request details
            cursor.execute("SELECT * FROM requests WHERE request_id = %s FOR UPDATE", (request_id,))
            request = cursor.fetchone()
            
            if not request or request['to_hospital_id'] != hospital_id:
                conn.rollback()
                cursor.close()
                conn.close()
                return False
            
            if request['status'] != 'PENDING':
                conn.rollback()
                cursor.close()
                conn.close()
                return False
            
            # Check inventory
            cursor.execute("""
            SELECT available_units FROM organ_inventory 
            WHERE hospital_id = %s AND organ_type = %s AND blood_group = %s
            FOR UPDATE
            """, (hospital_id, request['organ_type'], request['blood_group']))
            inventory = cursor.fetchone()
            
            if not inventory or inventory['available_units'] < request['quantity_requested']:
                conn.rollback()
                cursor.close()
                conn.close()
                return False
            
            # Update inventory (reduce stock)
            cursor.execute("""
            UPDATE organ_inventory 
            SET available_units = available_units - %s, last_updated = NOW()
            WHERE hospital_id = %s AND organ_type = %s AND blood_group = %s
            """, (request['quantity_requested'], hospital_id, request['organ_type'], request['blood_group']))
            
            # Update request status
            cursor.execute("""
            UPDATE requests 
            SET status = 'ACCEPTED', responded_at = NOW() 
            WHERE request_id = %s
            """, (request_id,))
            
            # Commit transaction
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            print(f"Error in accept_request: {e}")
            return False

    @staticmethod
    def reject_request(request_id, hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE requests 
        SET status = 'REJECTED', responded_at = NOW() 
        WHERE request_id = %s AND to_hospital_id = %s AND status = 'PENDING'
        """
        cursor.execute(query, (request_id, hospital_id))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

    @staticmethod
    def complete_request(request_id, hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE requests 
        SET status = 'COMPLETED' 
        WHERE request_id = %s AND from_hospital_id = %s AND status = 'ACCEPTED'
        """
        cursor.execute(query, (request_id, hospital_id))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

    @staticmethod
    def cancel_request(request_id, hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE requests 
        SET status = 'CANCELLED' 
        WHERE request_id = %s AND from_hospital_id = %s AND status = 'PENDING'
        """
        cursor.execute(query, (request_id, hospital_id))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

    @staticmethod
    def get_pending_count(hospital_id):
        """Get count of pending incoming requests"""
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) as count FROM requests 
        WHERE to_hospital_id = %s AND status = 'PENDING'
        """
        cursor.execute(query, (hospital_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def get_active_count(hospital_id):
        """Get count of active outgoing requests"""
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) as count FROM requests 
        WHERE from_hospital_id = %s AND status IN ('PENDING', 'ACCEPTED')
        """
        cursor.execute(query, (hospital_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 0


# Optional: Statistics class for dashboard
class Statistics:
    @staticmethod
    def get_hospital_stats(hospital_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        stats = {}
        
        # Inventory count
        cursor.execute("SELECT COUNT(*) as count FROM organ_inventory WHERE hospital_id = %s", (hospital_id,))
        stats['inventory_count'] = cursor.fetchone()['count']
        
        # Total available units
        cursor.execute("SELECT SUM(available_units) as total FROM organ_inventory WHERE hospital_id = %s", (hospital_id,))
        result = cursor.fetchone()
        stats['total_units'] = result['total'] if result['total'] else 0
        
        # Pending incoming requests
        cursor.execute("SELECT COUNT(*) as count FROM requests WHERE to_hospital_id = %s AND status = 'PENDING'", (hospital_id,))
        stats['pending_incoming'] = cursor.fetchone()['count']
        
        # Pending outgoing requests
        cursor.execute("SELECT COUNT(*) as count FROM requests WHERE from_hospital_id = %s AND status = 'PENDING'", (hospital_id,))
        stats['pending_outgoing'] = cursor.fetchone()['count']
        
        # Accepted requests
        cursor.execute("SELECT COUNT(*) as count FROM requests WHERE (from_hospital_id = %s OR to_hospital_id = %s) AND status = 'ACCEPTED'", (hospital_id, hospital_id))
        stats['active_requests'] = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return stats