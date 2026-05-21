import os
import sqlite3
from guest_dao import GuestDAO


def setup_test_database():
    """
    Set up a clean test database before running tests.
    
    Creates a fresh test database with the required tables.
    """
    db_path = 'ahs_database.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create fresh database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create Staff table (required for foreign keys in Reservation)
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
    
    # Insert dummy staff
    cursor.execute("INSERT INTO Staff (FirstName, LastName) VALUES ('John', 'Smith')")
    
    connection.commit()
    cursor.close()
    connection.close()


def test_create():
    """Test create method - Insert new guest."""
    print("Testing create()...")
    
    guest_dao = GuestDAO()
    
    guest_data = {
        'FirstName': 'Jane',
        'LastName': 'Doe',
        'PhoneNumber': '0412345678',
        'Email': 'jane@example.com',
        'CreditCardNum': '1234567890123456'
    }
    
    result = guest_dao.create(guest_data)
    
    assert result['status'] == 'Success', f"Create failed: {result['message']}"
    assert 'guest_id' in result, "guest_id not returned"
    assert result['guest_id'] == 1, "Expected first guest ID to be 1"
    
    print("✓ create() test passed")


def test_find_by_id():
    """Test find_by_id method - Retrieve single guest."""
    print("Testing find_by_id()...")
    
    guest_dao = GuestDAO()
    
    # Create a guest first
    guest_data = {
        'FirstName': 'John',
        'LastName': 'Smith',
        'PhoneNumber': '0498765432',
        'Email': 'john@example.com',
        'CreditCardNum': '9876543210987654'
    }
    
    create_result = guest_dao.create(guest_data)
    guest_id = create_result['guest_id']
    
    # Retrieve the guest
    result = guest_dao.find_by_id(guest_id)
    
    assert result['status'] == 'Success', f"Find failed: {result['message']}"
    assert result['data'] is not None, "No guest found"
    assert result['data']['FirstName'] == 'John', "First name mismatch"
    assert result['data']['Email'] == 'john@example.com', "Email mismatch"
    
    # Test finding non-existent guest
    result_not_found = guest_dao.find_by_id(9999)
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ find_by_id() test passed")


def test_find_all():
    """Test find_all method - Retrieve all guests."""
    print("Testing find_all()...")
    
    guest_dao = GuestDAO()
    
    # Create multiple guests
    guests_data = [
        {
            'FirstName': 'Alice',
            'LastName': 'Johnson',
            'PhoneNumber': '0412111111',
            'Email': 'alice@example.com',
            'CreditCardNum': '1111111111111111'
        },
        {
            'FirstName': 'Bob',
            'LastName': 'Williams',
            'PhoneNumber': '0412222222',
            'Email': 'bob@example.com',
            'CreditCardNum': '2222222222222222'
        }
    ]
    
    for guest in guests_data:
        guest_dao.create(guest)
    
    # Retrieve all guests
    result = guest_dao.find_all()
    
    assert result['status'] == 'Success', f"Find all failed: {result['message']}"
    assert isinstance(result['data'], list), "Data should be a list"
    assert len(result['data']) >= 2, "Should have at least 2 guests"
    
    print("✓ find_all() test passed")


def test_find_ids():
    """Test find_ids method - Get IDs and names for dropdown."""
    print("Testing find_ids()...")
    
    guest_dao = GuestDAO()
    
    result = guest_dao.find_ids()
    
    assert result['status'] == 'Success', f"Find IDs failed: {result['message']}"
    assert isinstance(result['data'], list), "Data should be a list"
    
    if len(result['data']) > 0:
        assert 'GuestID' in result['data'][0], "GuestID should be in result"
        assert 'FullName' in result['data'][0], "FullName should be in result"
    
    print("✓ find_ids() test passed")


def test_update():
    """Test update method - Modify existing guest."""
    print("Testing update()...")
    
    guest_dao = GuestDAO()
    
    # Create a guest
    guest_data = {
        'FirstName': 'David',
        'LastName': 'Brown',
        'PhoneNumber': '0413333333',
        'Email': 'david@example.com',
        'CreditCardNum': '3333333333333333'
    }
    
    create_result = guest_dao.create(guest_data)
    guest_id = create_result['guest_id']
    
    # Update the guest
    update_data = {
        'Email': 'david.new@example.com',
        'PhoneNumber': '0414444444'
    }
    
    result = guest_dao.update(guest_id, update_data)
    
    assert result['status'] == 'Success', f"Update failed: {result['message']}"
    
    # Verify the update
    verify_result = guest_dao.find_by_id(guest_id)
    assert verify_result['data']['Email'] == 'david.new@example.com', "Email not updated"
    assert verify_result['data']['PhoneNumber'] == '0414444444', "Phone not updated"
    
    # Test updating non-existent guest
    result_not_found = guest_dao.update(9999, {'FirstName': 'Test'})
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ update() test passed")


def test_delete():
    """Test delete method - Remove guest."""
    print("Testing delete()...")
    
    guest_dao = GuestDAO()
    
    # Create a guest
    guest_data = {
        'FirstName': 'Emma',
        'LastName': 'Green',
        'PhoneNumber': '0415555555',
        'Email': 'emma@example.com',
        'CreditCardNum': '5555555555555555'
    }
    
    create_result = guest_dao.create(guest_data)
    guest_id = create_result['guest_id']
    
    # Delete the guest
    result = guest_dao.delete(guest_id)
    
    assert result['status'] == 'Success', f"Delete failed: {result['message']}"
    
    # Verify deletion
    verify_result = guest_dao.find_by_id(guest_id)
    assert verify_result['status'] == 'Not Found', "Guest should be deleted"
    
    # Test deleting non-existent guest
    result_not_found = guest_dao.delete(9999)
    assert result_not_found['status'] == 'Not Found', "Should return Not Found for invalid ID"
    
    print("✓ delete() test passed")


def main():
    """
    Run all Guest DAO tests.
    
    Sets up test database, runs all test methods, and reports results.
    """
    print("\n" + "="*50)
    print("Guest DAO - Test Suite")
    print("="*50 + "\n")
    
    try:
        setup_test_database()
        
        test_create()
        test_find_by_id()
        test_find_all()
        test_find_ids()
        test_update()
        test_delete()
        
        print("\n" + "="*50)
        print("✓ All Guest DAO tests PASSED!")
        print("="*50 + "\n")
    
    except AssertionError as e:
        print(f"\n✗ Test FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        raise


if __name__ == "__main__":
    main()
