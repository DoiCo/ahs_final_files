import sqlite3
import os


def create_database():
    """
    Create the AHS database and initialise all tables with proper foreign key constraints.
    
    Tables created:
    - Staff: Office staff members (no foreign keys)
    - Guest: Hotel guests (no foreign keys)
    - Reservation: Guest reservations (with foreign keys to Staff and Guest)
    
    Returns:
        None
    
    Raises:
        sqlite3.Error: If database operations fail
    """
    db_path = 'ahs_database.db'
    
    try:
        # Remove existing database for fresh setup (comment out for production)
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Connect to database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Create Staff table
        cursor.execute("""
            CREATE TABLE Staff (
                StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL
            );
        """)
        
        # Create Guest table
        cursor.execute("""
            CREATE TABLE Guest (
                GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                PhoneNumber TEXT NOT NULL,
                Email TEXT NOT NULL,
                CreditCardNum TEXT NOT NULL
            );
        """)
        
        # Create Reservation table with foreign keys
        cursor.execute("""
            CREATE TABLE Reservation (
                ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                GuestID INTEGER NOT NULL,
                StaffID INTEGER NOT NULL,
                CheckInDate TEXT NOT NULL,
                CheckOutDate TEXT NOT NULL,
                NumAdults INTEGER NOT NULL,
                NumChildren INTEGER NOT NULL,
                NumInfants INTEGER NOT NULL,
                PromoCode TEXT,
                FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
                FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
            );
        """)
        
        # Insert dummy staff data (required for foreign key constraints)
        staff_data = [
            ('John', 'Smith'),
            ('Sarah', 'Johnson'),
            ('Michael', 'Williams'),
            ('Emily', 'Brown'),
            ('David', 'Jones')
        ]
        
        cursor.executemany(
            "INSERT INTO Staff (FirstName, LastName) VALUES (?, ?)",
            staff_data
        )
        
        # Commit all changes
        connection.commit()
        print("✓ Database created successfully: ahs_database.db")
        print("✓ Tables created: Staff, Guest, Reservation")
        print("✓ Dummy staff data inserted (5 staff members)")
        print("✓ Foreign key constraints enabled")
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        raise
    
    finally:
        # Ensure cursor and connection are properly closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_database()
