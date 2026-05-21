import sqlite3


class ReservationDAO:
    """Data Access Object for reservation table operations."""
    
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
    
    def create(self, data):
        """Insert a new reservation record into the database."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO Reservation 
                (GuestID, StaffID, CheckInDate, CheckOutDate, NumAdults, 
                 NumChildren, NumInfants, PromoCode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('GuestID'),
                data.get('StaffID'),
                data.get('CheckInDate'),
                data.get('CheckOutDate'),
                data.get('NumAdults'),
                data.get('NumChildren'),
                data.get('NumInfants'),
                data.get('PromoCode')
            ))
            
            self.connection.commit()
            reservation_id = cursor.lastrowid
            
            return {
                'status': 'Success',
                'message': f'Reservation {reservation_id} created successfully',
                'reservation_id': reservation_id
            }
        
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Foreign key violation: {e}'}
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Failed to create reservation: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_by_id(self, reservation_id):
        """Retrieve a reservation record by ID with guest and staff information."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT 
                    r.ReservationID,
                    r.GuestID,
                    g.FirstName || ' ' || g.LastName AS GuestName,
                    r.StaffID,
                    s.FirstName || ' ' || s.LastName AS StaffName,
                    r.CheckInDate,
                    r.CheckOutDate,
                    r.NumAdults,
                    r.NumChildren,
                    r.NumInfants,
                    r.PromoCode
                FROM Reservation r
                LEFT JOIN Guest g ON r.GuestID = g.GuestID
                LEFT JOIN Staff s ON r.StaffID = s.StaffID
                WHERE r.ReservationID = ?
            """, (reservation_id,))
            
            row = cursor.fetchone()
            
            if row:
                reservation_data = dict(row)
                return {
                    'status': 'Success',
                    'message': 'Reservation found',
                    'data': reservation_data
                }
            else:
                return {
                    'status': 'Not Found',
                    'message': f'No reservation found with ID {reservation_id}',
                    'data': None
                }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving reservation: {e}', 'data': None}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_all(self):
        """Retrieve all reservations with joined guest and staff names."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT 
                    r.ReservationID,
                    r.GuestID,
                    g.FirstName || ' ' || g.LastName AS GuestName,
                    r.StaffID,
                    s.FirstName || ' ' || s.LastName AS StaffName,
                    r.CheckInDate,
                    r.CheckOutDate,
                    r.NumAdults,
                    r.NumChildren,
                    r.NumInfants,
                    r.PromoCode
                FROM Reservation r
                LEFT JOIN Guest g ON r.GuestID = g.GuestID
                LEFT JOIN Staff s ON r.StaffID = s.StaffID
                ORDER BY r.ReservationID
            """)
            
            rows = cursor.fetchall()
            reservations = [dict(row) for row in rows]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(reservations)} reservation(s)',
                'data': reservations
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving reservations: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def find_ids(self):
        """Retrieve all reservation IDs for reference purposes."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(
                "SELECT ReservationID FROM Reservation ORDER BY ReservationID")
            rows = cursor.fetchall()
            
            reservation_ids = [row[0] for row in rows]
            
            return {
                'status': 'Success',
                'message': f'Retrieved {len(reservation_ids)} reservation(s)',
                'data': reservation_ids
            }
        
        except sqlite3.Error as e:
            return {'status': 'Error', 'message': f'Error retrieving reservation IDs: {e}', 'data': []}
        
        finally:
            if cursor:
                cursor.close()
    
    def update(self, reservation_id, data):
        """
        Update an existing reservation record.
        
        Args:
            reservation_id (int): The ID of the reservation to update
            data (dict): Dictionary containing fields to update
        
        Returns:
            dict: Status dictionary with keys:
                - 'status': 'Success', 'Not Found', or 'Error'
                - 'message': Description of operation result
        """
        cursor = None
        allowed_fields = {'GuestID', 'StaffID', 'CheckInDate', 'CheckOutDate',
                         'NumAdults', 'NumChildren', 'NumInfants', 'PromoCode'}
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(
                "SELECT ReservationID FROM Reservation WHERE ReservationID = ?",
                (reservation_id,))
            if not cursor.fetchone():
                return {
                    'status': 'Not Found',
                    'message': f'No reservation found with ID {reservation_id}'
                }
            
            valid_updates = {k: v for k, v in data.items()
                            if k in allowed_fields}
            if not valid_updates:
                return {
                    'status': 'Error',
                    'message': 'No valid fields to update'
                }
            
            set_clause = ', '.join([f"{key} = ?" for key in valid_updates])
            values = list(valid_updates.values()) + [reservation_id]
            
            cursor.execute(
                f"UPDATE Reservation SET {set_clause} WHERE ReservationID = ?",
                values)
            self.connection.commit()
            
            return {
                'status': 'Success',
                'message': f'Reservation ID {reservation_id} updated successfully'
            }
        
        except sqlite3.IntegrityError as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Foreign key violation: {e}'}
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error',
                    'message': f'Failed to update reservation: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def delete(self, reservation_id):
        """Delete a reservation record from the database."""
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(
                "SELECT ReservationID FROM Reservation WHERE ReservationID = ?",
                (reservation_id,))
            if not cursor.fetchone():
                return {
                    'status': 'Not Found',
                    'message': f'No reservation found with ID {reservation_id}'
                }
            
            cursor.execute("DELETE FROM Reservation WHERE ReservationID = ?",
                          (reservation_id,))
            self.connection.commit()
            
            return {
                'status': 'Success',
                'message': f'Reservation ID {reservation_id} deleted successfully'
            }
        
        except sqlite3.Error as e:
            self.connection.rollback()
            return {'status': 'Error', 'message': f'Failed to delete reservation: {e}'}
        
        finally:
            if cursor:
                cursor.close()
    
    def __del__(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
