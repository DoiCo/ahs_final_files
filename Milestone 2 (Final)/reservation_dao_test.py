import os
import sqlite3
from reservation_dao import ReservationDAO
from guest_dao import GuestDAO
from staff_dao import StaffDAO


def setup_test_database():
    """
    Set up a clean test database before running tests.
    
    Creates a fresh test database with required tables and sample data.
    """
    db_path = 'ahs_database.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create fresh database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
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
    
    # Create Reservation table
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
    
    # Insert test staff
    cursor.execute("INSERT INTO Staff (FirstName, LastName) VALUES ('John', 'Smith')")
    cursor.execute("INSERT INTO Staff (FirstName, LastName) VALUES ('Sarah', 'Johnson')")
    
    # Insert test guests
    cursor.execute("""
        INSERT INTO Guest (FirstName, LastName, PhoneNumber, Email, CreditCardNum)
        VALUES ('Jane', 'Doe', '0412345678', 'jane@example.com', '1234567890123456')
    """)
    cursor.execute("""
        INSERT INTO Guest (FirstName, LastName, PhoneNumber, Email, CreditCardNum)
        VALUES ('Bob', 'Smith', '0498765432', 'bob@example.com', '9876543210987654')
    """)
    
    connection.commit()
    cursor.close()
    connection.close()


def test_create():
    """Test create method - Insert new reservation."""
    print("Testing create()...")
    
    reservation_dao = ReservationDAO()
    
    reservation_data = {
        'GuestID': 1,
        'StaffID': 1,
        'CheckInDate': '2026-06-01',
        'CheckOutDate': '2026-06-05',
        'NumAdults': 2,
        'NumChildren': 1,
        'NumInfants': 0,
        'PromoCode': 'SUMMER20'
    }
    
    result = reservation_dao.create(reservation_data)
    
    assert result['status'] == 'Success', f"Create failed: {result['message']}"
    assert 'reservation_id' in result, "reservation_id not returned"
    assert result['reservation_id'] == 1, "Expected first reservation ID to be 1"
    
    print("✓ create() test passed")


def test_create_invalid_foreign_key():
    """Test create method with invalid foreign key."""
    print("Testing create() with invalid foreign key...")
    
    reservation_dao = ReservationDAO()
    
    reservation_data = {
        'GuestID': 9999,  # Non-existent guest
        'StaffID': 1,
        'CheckInDate': '2026-06-01',
        'CheckOutDate': '2026-06-05',
        'NumAdults': 2,
        'NumChildren': 0,
        'NumInfants': 0,
        'PromoCode': None
    }
    
    result = reservation_dao.create(reservation_data)
    
    assert result['status'] == 'Error', "Should fail with invalid foreign key"
    
    print("✓ create() invalid FK test passed")


def test_find_by_id():
    """Test find_by_id method - Retrieve single reservation."""
    print("Testing find_by_id()...")
    
    reservation_dao = ReservationDAO()
    
    # Create a reservation first
    reservation_data = {
        'GuestID': 1,
        'StaffID': 1,
        'CheckInDate': '2026-07-01',
        'CheckOutDate': '2026-07-05',
        'NumAdults': 1,
        'NumChildren': 0,
        'NumInfants': 0,
        'PromoCode': 'SUMMER25'
    }
    
    create_result = reservation_dao.create(reservation_data)
    reservation_id = create_result['reservation_id']
    
    # Retrieve the reservation
    result = reservation_dao.find_by_id(reservation_id)
    
    assert result['status'] == 'Success', f"Find failed: {result['message']}"
    assert result['data'] is not None, "No reservation found"
    assert result['data']['GuestName'] == 'Jane Doe', "Guest name mismatch"
    assert result['data']['CheckInDate'] == '2026-07-01', "Check-in date mismatch"
    
    # Test finding non-existent reservation
    result_not_found = reservation_dao.find_by_id(9999)
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ find_by_id() test passed")


def test_find_all():
    """Test find_all method - Retrieve all reservations with JOINs."""
    print("Testing find_all()...")
    
    reservation_dao = ReservationDAO()
    
    # Create multiple reservations
    reservations_data = [
        {
            'GuestID': 1,
            'StaffID': 1,
            'CheckInDate': '2026-08-01',
            'CheckOutDate': '2026-08-03',
            'NumAdults': 2,
            'NumChildren': 0,
            'NumInfants': 0,
            'PromoCode': None
        },
        {
            'GuestID': 2,
            'StaffID': 2,
            'CheckInDate': '2026-08-05',
            'CheckOutDate': '2026-08-08',
            'NumAdults': 1,
            'NumChildren': 1,
            'NumInfants': 1,
            'PromoCode': 'FAMILY10'
        }
    ]
    
    for res in reservations_data:
        reservation_dao.create(res)
    
    # Retrieve all reservations
    result = reservation_dao.find_all()
    
    assert result['status'] == 'Success', f"Find all failed: {result['message']}"
    assert isinstance(result['data'], list), "Data should be a list"
    assert len(result['data']) >= 2, "Should have at least 2 reservations"
    
    # Verify JOINs worked (should have guest and staff names, not just IDs)
    for res in result['data']:
        assert 'GuestName' in res, "GuestName should be joined"
        assert 'StaffName' in res, "StaffName should be joined"
        assert 'Jane Doe' in res['GuestName'] or 'Bob Smith' in res['GuestName'], "Guest name should be populated"
    
    print("✓ find_all() test passed")


def test_find_ids():
    """Test find_ids method - Get reservation IDs."""
    print("Testing find_ids()...")
    
    reservation_dao = ReservationDAO()
    
    result = reservation_dao.find_ids()
    
    assert result['status'] == 'Success', f"Find IDs failed: {result['message']}"
    assert isinstance(result['data'], list), "Data should be a list"
    
    print("✓ find_ids() test passed")


def test_update():
    """Test update method - Modify existing reservation."""
    print("Testing update()...")
    
    reservation_dao = ReservationDAO()
    
    # Create a reservation
    reservation_data = {
        'GuestID': 1,
        'StaffID': 1,
        'CheckInDate': '2026-09-01',
        'CheckOutDate': '2026-09-05',
        'NumAdults': 2,
        'NumChildren': 0,
        'NumInfants': 0,
        'PromoCode': 'EARLY50'
    }
    
    create_result = reservation_dao.create(reservation_data)
    reservation_id = create_result['reservation_id']
    
    # Update the reservation
    update_data = {
        'NumAdults': 3,
        'NumChildren': 1,
        'PromoCode': 'UPDATED20'
    }
    
    result = reservation_dao.update(reservation_id, update_data)
    
    assert result['status'] == 'Success', f"Update failed: {result['message']}"
    
    # Verify the update
    verify_result = reservation_dao.find_by_id(reservation_id)
    assert verify_result['data']['NumAdults'] == 3, "NumAdults not updated"
    assert verify_result['data']['NumChildren'] == 1, "NumChildren not updated"
    
    # Test updating non-existent reservation
    result_not_found = reservation_dao.update(9999, {'NumAdults': 5})
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ update() test passed")


def test_delete():
    """Test delete method - Remove reservation."""
    print("Testing delete()...")
    
    reservation_dao = ReservationDAO()
    
    # Create a reservation
    reservation_data = {
        'GuestID': 2,
        'StaffID': 2,
        'CheckInDate': '2026-10-01',
        'CheckOutDate': '2026-10-04',
        'NumAdults': 1,
        'NumChildren': 0,
        'NumInfants': 0,
        'PromoCode': None
    }
    
    create_result = reservation_dao.create(reservation_data)
    reservation_id = create_result['reservation_id']
    
    # Delete the reservation
    result = reservation_dao.delete(reservation_id)
    
    assert result['status'] == 'Success', f"Delete failed: {result['message']}"
    
    # Verify deletion
    verify_result = reservation_dao.find_by_id(reservation_id)
    assert verify_result['status'] == 'Not Found', "Reservation should be deleted"
    
    # Test deleting non-existent reservation
    result_not_found = reservation_dao.delete(9999)
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ delete() test passed")


def main():
    """
    Run all Reservation DAO tests.
    
    Sets up test database, runs all test methods, and reports results.
    """
    print("\n" + "="*50)
    print("Reservation DAO - Test Suite")
    print("="*50 + "\n")
    
    try:
        setup_test_database()
        
        test_create()
        test_create_invalid_foreign_key()
        test_find_by_id()
        test_find_all()
        test_find_ids()
        test_update()
        test_delete()
        
        print("\n" + "="*50)
        print("✓ All Reservation DAO tests PASSED!")
        print("="*50 + "\n")
    
    except AssertionError as e:
        print(f"\n✗ Test FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        raise


if __name__ == "__main__":
    main()
