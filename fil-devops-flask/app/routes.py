from flask import Blueprint, request, jsonify
from app.models import BankTransaction
from datetime import datetime

# Create a blueprint for API routes
api = Blueprint('api', __name__)


@api.route('/getall', methods=['GET'])
def get_all():
    """Get all transactions"""
    try:
        transactions = BankTransaction.get_all()
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/getById/<custId>', methods=['GET'])
def get_by_id(custId):
    """Get transactions by customer ID"""
    try:
        transactions = BankTransaction.get_by_cust_id(custId)
        if not transactions:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/getByTransId/<transId>', methods=['GET'])
def get_by_trans_id(transId):
    """Get transaction by transaction ID"""
    try:
        transaction = BankTransaction.get_by_trans_id(transId)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify(transaction), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/getByDate/<from_date>/<to_date>', methods=['GET'])
def get_by_date_range(from_date, to_date):
    """Get transactions between two dates"""
    try:
        # Basic date validation
        datetime.strptime(from_date, '%Y-%m-%d')
        datetime.strptime(to_date, '%Y-%m-%d')

        transactions = BankTransaction.get_by_date(from_date, to_date)
        return jsonify(transactions), 200
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/transaction', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.get_json()
        required_fields = ['bank_id', 'bank_name', 'bank_ifs_code',
                           'cust_id', 'cust_name', 'cust_amt', 'acct_type']

        # Check if all required fields are present
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        if BankTransaction.create_transaction(data):
            return jsonify({"message": "Transaction created successfully"}), 201
        return jsonify({"error": "Failed to create transaction"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
