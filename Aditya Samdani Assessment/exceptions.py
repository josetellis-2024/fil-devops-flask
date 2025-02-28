class InvalidTransactionIdError(Exception):
    code=400
    message="Invalid transaction ID"

class TransactionNotFoundError(Exception):
    code=404
    message="Transaction not found"

class InvalidDateError(Exception):
    code=400
    message="Invalid date format"

class InternalServerError(Exception):
    code=500
    message="Internal server error"
