from datetime import datetime
import random


def generate_transaction_id():
    """Generates a random 12-digit transaction ID"""
    return str(random.randint(100000000000, 999999999999))


def validate_date(date_string):
    """Check if date string is valid (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_amount(amount):
    """Format amount with ₹ symbol"""
    return f"₹{amount:.2f}"
