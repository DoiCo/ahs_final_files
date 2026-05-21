from validation import Validation


def test_is_numeric():
    """Test is_numeric method with valid and invalid inputs."""
    print("Testing is_numeric()...")
    
    # Valid cases
    assert Validation.is_numeric("12345") == True
    assert Validation.is_numeric("0") == True
    assert Validation.is_numeric("9999999999") == True
    
    # Invalid cases
    assert Validation.is_numeric("12a45") == False
    assert Validation.is_numeric("123.45") == False
    assert Validation.is_numeric("") == False
    assert Validation.is_numeric("  ") == False
    assert Validation.is_numeric(None) == False
    
    print("✓ is_numeric() tests passed")


def test_is_alphabetic():
    """Test is_alphabetic method with valid and invalid inputs."""
    print("Testing is_alphabetic()...")
    
    # Valid cases
    assert Validation.is_alphabetic("John") == True
    assert Validation.is_alphabetic("Mary Smith") == True
    assert Validation.is_alphabetic("A") == True
    assert Validation.is_alphabetic("abc XYZ") == True
    
    # Invalid cases
    assert Validation.is_alphabetic("John123") == False
    assert Validation.is_alphabetic("John-Smith") == False
    assert Validation.is_alphabetic("") == False
    assert Validation.is_alphabetic("123") == False
    assert Validation.is_alphabetic(None) == False
    
    print("✓ is_alphabetic() tests passed")


def test_is_alphanumeric():
    """Test is_alphanumeric method with valid and invalid inputs."""
    print("Testing is_alphanumeric()...")
    
    # Valid cases
    assert Validation.is_alphanumeric("Test123") == True
    assert Validation.is_alphanumeric("ABC 123") == True
    assert Validation.is_alphanumeric("a b c 1 2 3") == True
    
    # Invalid cases
    assert Validation.is_alphanumeric("Test-123") == False
    assert Validation.is_alphanumeric("Test@123") == False
    assert Validation.is_alphanumeric("") == False
    assert Validation.is_alphanumeric(None) == False
    
    print("✓ is_alphanumeric() tests passed")


def test_is_phone_number():
    """Test is_phone_number method with Australian format."""
    print("Testing is_phone_number()...")
    
    # Valid Australian phone formats
    assert Validation.is_phone_number("0412345678") == True
    assert Validation.is_phone_number("0298765432") == True
    assert Validation.is_phone_number("04 1234 5678") == True
    
    # Invalid formats
    assert Validation.is_phone_number("123456789") == False  # Missing leading 0
    assert Validation.is_phone_number("041234567") == False   # Only 9 digits
    assert Validation.is_phone_number("04123456789") == False # 11 digits
    assert Validation.is_phone_number("04-1234-5678") == False  # Wrong separator
    assert Validation.is_phone_number("") == False
    assert Validation.is_phone_number(None) == False
    
    print("✓ is_phone_number() tests passed")


def test_is_email():
    """Test is_email method with valid and invalid formats."""
    print("Testing is_email()...")
    
    # Valid email formats
    assert Validation.is_email("user@example.com") == True
    assert Validation.is_email("john.doe@company.co.uk") == True
    assert Validation.is_email("test123@test.org") == True
    assert Validation.is_email("a@b.co") == True
    
    # Invalid email formats
    assert Validation.is_email("invalid.email") == False  # No @
    assert Validation.is_email("@example.com") == False   # No local part
    assert Validation.is_email("user@") == False          # No domain
    assert Validation.is_email("user @example.com") == False  # Space in local
    assert Validation.is_email("user@.com") == False      # Missing domain name
    assert Validation.is_email("") == False
    assert Validation.is_email(None) == False
    
    print("✓ is_email() tests passed")


def test_is_valid_date():
    """Test is_valid_date method with various date formats."""
    print("Testing is_valid_date()...")
    
    # Valid dates
    assert Validation.is_valid_date("2026-05-20") == True
    assert Validation.is_valid_date("2025-01-01") == True
    assert Validation.is_valid_date("2026-12-31") == True
    assert Validation.is_valid_date("2024-02-29") == True  # Leap year
    
    # Invalid dates - format
    assert Validation.is_valid_date("20/05/2026") == False  # Wrong format
    assert Validation.is_valid_date("2026-5-20") == False   # Missing leading zero
    assert Validation.is_valid_date("26-05-20") == False    # 2-digit year
    
    # Invalid dates - values
    assert Validation.is_valid_date("2026-13-01") == False  # Invalid month
    assert Validation.is_valid_date("2026-00-15") == False  # Invalid month
    assert Validation.is_valid_date("2026-02-30") == False  # Invalid day
    assert Validation.is_valid_date("2025-02-29") == False  # Not a leap year
    assert Validation.is_valid_date("2026-05-00") == False  # Invalid day
    
    # Invalid dates - out of range
    assert Validation.is_valid_date("2019-05-20") == False  # Before 2020
    assert Validation.is_valid_date("2051-05-20") == False  # After 2050
    
    # Invalid dates - empty
    assert Validation.is_valid_date("") == False
    assert Validation.is_valid_date(None) == False
    
    print("✓ is_valid_date() tests passed")


def test_is_credit_card_number():
    """Test is_credit_card_number method."""
    print("Testing is_credit_card_number()...")
    
    # Valid credit card format (16 digits)
    assert Validation.is_credit_card_number("1234567890123456") == True
    assert Validation.is_credit_card_number("0000000000000000") == True
    
    # Invalid credit card formats
    assert Validation.is_credit_card_number("123456789012345") == False  # 15 digits
    assert Validation.is_credit_card_number("12345678901234567") == False  # 17 digits
    assert Validation.is_credit_card_number("123456789012345a") == False  # Non-numeric
    assert Validation.is_credit_card_number("1234-5678-9012-3456") == False  # With hyphens
    assert Validation.is_credit_card_number("") == False
    assert Validation.is_credit_card_number(None) == False
    
    print("✓ is_credit_card_number() tests passed")


def main():
    """
    Run all validation tests.
    
    Prints test results and summary. Exits with success code if
    all tests pass.
    """
    print("\n" + "="*50)
    print("Validation Module - Test Suite")
    print("="*50 + "\n")
    
    try:
        test_is_numeric()
        test_is_alphabetic()
        test_is_alphanumeric()
        test_is_phone_number()
        test_is_email()
        test_is_valid_date()
        test_is_credit_card_number()
        
        print("\n" + "="*50)
        print("✓ All validation tests PASSED!")
        print("="*50 + "\n")
    
    except AssertionError as e:
        print(f"\n✗ Test FAILED: {e}\n")
        raise


if __name__ == "__main__":
    main()
