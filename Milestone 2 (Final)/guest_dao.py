import sqlite3


class GuestDAO:
    """Data Access Object for guest table operations."""
    
    def __init__(self):
        """Initialise database connection and enable foreign keys."""
        self.db_path = 'ahs_database.db'
        self.connection = None
        
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.close()
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Connection failed: {e}'}
    
    def create(self, data):
        """Insert a new guest record into the database."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO Guest (FirstName, LastName, PhoneNumber, Email, CreditCardNum)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data.get('FirstName'),
                data.get('LastName'),
                data.get('PhoneNumber'),
                data.get('Email'),
                data.get('CreditCardNum')
            ))
            
            self.connection.commit()
            guest_id = cursor.lastrowid
            
            return {
                'status': 'Success',
                'message': f'Guest {data.get("FirstName")} {data.get("LastName")} added successfully',
                'guest_id': guest_id
            }
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Failed to create guest: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_by_id(self, guest_id):
        """Retrieve a guest record by ID."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT * FROM Guest WHERE GuestID = ?
            """, (guest_id,))
            
            row = cursor.fetchone()
            
            if row:
                guest_data = dict(row)
                return {
                    'status': 'Success',
                    'message': 'Guest found',
                    'data': guest_data
                }
            else:
                return {
                    'status': 'Not Found',
                    'message': f'No guest found with ID {guest_id}',
                    'data': None
                }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving guest: {e}', 'data': None}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_all(self):
        """Retrieve all guest records from the database."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT * FROM Guest ORDER BY GuestID")
            rows = cursor.fetchall()
            
            guests = [dict(row) for row in rows]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(guests)} guest(s)',
                'data': guests
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving guests: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_ids(self):
        """Retrieve guest IDs and names for dropdown population."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT GuestID, FirstName, LastName 
                FROM Guest 
                ORDER BY GuestID
            """)
            
            rows = cursor.fetchall()
            
            guest_ids = [
                {
                    'GuestID': row[0],
                    'FullName': f"{row[1]} {row[2]}"
                }
                for row in rows
            ]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(guest_ids)} guest(s)',
                'data': guest_ids
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving guest IDs: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def update(self, guest_id, data):
        """Update guest record with provided data."""
        cursor = None
        allowed_fields = {'FirstName', 'LastName', 'PhoneNumber', 'Email',
                         'CreditCardNum'}
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT GuestID FROM Guest WHERE GuestID = ?",
                          (guest_id,))
            if not cursor.fetchone():
                return {
                    'status': 'Not Found',
                    'message': f'No guest found with ID {guest_id}'
                }
            
            valid_updates = {k: v for k, v in data.items()
                            if k in allowed_fields}
            if not valid_updates:
                return {
                    'status': 'Error',
                    'message': 'No valid fields to update'
                }
            
            set_clause = ', '.join([f"{key} = ?" for key in valid_updates])
            values = list(valid_updates.values()) + [guest_id]
            
            cursor.execute(f"UPDATE Guest SET {set_clause} WHERE GuestID = ?",
                          values)
            self.connection.commit()
            
            return {
                'status': 'Success',
                'message': f'Guest ID {guest_id} updated successfully'
            }
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Failed to update guest: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def delete(self, guest_id):
        """Delete guest record by ID."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT GuestID FROM Guest WHERE GuestID = ?",
                          (guest_id,))
            if not cursor.fetchone():
                return {
                    'status': 'Not Found',
                    'message': f'No guest found with ID {guest_id}'
                }
            
            cursor.execute("DELETE FROM Guest WHERE GuestID = ?", (guest_id,))
            self.connection.commit()
            
            return {
                'status': 'Success',
                'message': f'Guest ID {guest_id} deleted successfully'
            }
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Failed to delete guest: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def __del__(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
