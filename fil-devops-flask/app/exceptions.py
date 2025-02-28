# app/exceptions.py

class BankException(Exception):
    """Base exception class for all banking operations"""

    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RecordNotFoundError(BankException):
    """Exception raised when a requested record is not found"""

    def __init__(self, message="Requested record not found"):
        super().__init__(message, status_code=404)


class InvalidTransactionIdError(BankException):
    """Exception raised when transaction ID format is invalid"""

    def __init__(self, message="Transaction ID must be a 12-digit number"):
        super().__init__(message, status_code=400)


class DatabaseConnectionError(BankException):
    """Exception raised when connection to Snowflake fails"""

    def __init__(self, message="Failed to connect to database"):
        super().__init__(message, status_code=500)


class InvalidDateFormatError(BankException):
    """Exception raised when date format is invalid"""

    def __init__(self, message="Invalid date format. Use YYYY-MM-DD"):
        super().__init__(message, status_code=400)
