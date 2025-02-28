import logging
from flask import jsonify

# Set up logging
logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class NotFoundError(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

class BadRequestError(Exception):
    def __init__(self, message="Bad Request"):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    def __init__(self, message="Database error occurred"):
        self.message = message
        super().__init__(self.message)

def handle_exception(error):
    logging.error(f"Error: {str(error)}")
    
    if isinstance(error, NotFoundError):
        return jsonify({"error": "Not Found", "message": error.message}), 404
    elif isinstance(error, BadRequestError):
        return jsonify({"error": "Bad Request", "message": error.message}), 400
    elif isinstance(error, DatabaseError):
        return jsonify({"error": "Database Error", "message": error.message}), 500
    else:
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong!"}), 500
