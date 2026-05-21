import sqlite3


class StaffDAO:
    """Data Access Object for staff table operations."""
    
    def __init__(self):
        """Initialize database connection and enable foreign keys."""
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
    
    def find_all(self):
        """Retrieve all staff records from the database."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT * FROM Staff ORDER BY StaffID")
            rows = cursor.fetchall()
            
            staff = [dict(row) for row in rows]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(staff)} staff member(s)',
                'data': staff
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving staff: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_ids(self):
        """Retrieve staff IDs and names for dropdown population."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT StaffID, FirstName, LastName 
                FROM Staff 
                ORDER BY StaffID
            """)
            
            rows = cursor.fetchall()
            
            staff_ids = [
                {
                    'StaffID': row[0],
                    'FullName': f"{row[1]} {row[2]}"
                }
                for row in rows
            ]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(staff_ids)} staff member(s)',
                'data': staff_ids
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving staff IDs: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def __del__(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
