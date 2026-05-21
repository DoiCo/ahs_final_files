import re


class Validation:
    """Static validation methods for user input."""
    
    @staticmethod
    def is_numeric(value):
        """Return True if value contains only digits."""
        if not isinstance(value, str) or value == "":
            return False
        return value.isdigit()
    
    @staticmethod
    def is_alphabetic(value):
        """Return True if value contains only letters and spaces."""
        if not isinstance(value, str) or value == "":
            return False
        return all(char.isalpha() or char.isspace() for char in value)
    
    @staticmethod
    def is_alphanumeric(value):
        """Return True if value contains only letters, numbers, and spaces."""
        if not isinstance(value, str) or value == "":
            return False
        return all(char.isalnum() or char.isspace() for char in value)
    
    @staticmethod
    def is_phone_number(value):
        """Validate Australian phone number (10 digits, with optional spaces)."""
        if not isinstance(value, str) or value == "":
            return False
        pattern = r'^0\d{9}$|^0\d{1}\s\d{4}\s\d{4}$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def is_email(value):
        """Validate email address format."""
        if not isinstance(value, str) or value == "":
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def is_valid_date(date_str):
        """Validate date string in YYYY-MM-DD format."""
        if not isinstance(date_str, str) or date_str == "":
            return False
        
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            return False
        
        try:
            year, month, day = map(int, date_str.split('-'))
            
            if year < 2020 or year > 2050:
                return False
            
            if month < 1 or month > 12:
                return False
            
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month[1] = 29
            
            if day < 1 or day > days_in_month[month - 1]:
                return False
            
            return True
        
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def is_credit_card_number(value):
        """Validate credit card number (16 digits)."""
        if not isinstance(value, str) or value == "":
            return False
        return value.isdigit() and len(value) == 16
