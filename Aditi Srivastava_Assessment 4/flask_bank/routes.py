from flask import Blueprint, request, jsonify
from db import get_snowflake_connection

routes = Blueprint('routes', __name__)

@routes.route('/v1/gpay/create', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        # Set the active database and schema
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        insert_query = """
            INSERT INTO bank_transactions 
            (bank_id, bank_name, bank_ifsc, cust_amt, acct_type, transaction_date, transaction_id, transaction_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('bank_id'),
            data.get('bank_name'),
            data.get('bank_ifsc'),
            data.get('cust_amt'),
            data.get('acct_type'),
            data.get('transaction_date'),
            data.get('transaction_id'),
            data.get('transaction_status')
        )
        cursor.execute(insert_query, params)
        conn.commit()
        return jsonify({"message": "Transaction created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/getall', methods=['GET'])
def get_all_transactions():
    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        cursor.execute("SELECT * FROM bank_transactions")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/getByID/<bank_id>', methods=['GET'])
def get_transaction_by_bank_id(bank_id):
    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        query = "SELECT * FROM bank_transactions WHERE bank_id = %s"
        cursor.execute(query, (bank_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, row))
            return jsonify(result), 200
        else:
            return jsonify({"message": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/getByTransID/<transaction_id>', methods=['GET'])
def get_transaction_by_trans_id(transaction_id):
    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        query = "SELECT * FROM bank_transactions WHERE transaction_id = %s"
        cursor.execute(query, (transaction_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, row))
            return jsonify(result), 200
        else:
            return jsonify({"message": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/getByDate', methods=['GET'])
def get_transactions_by_date():
    # Expecting 'from' and 'to' query parameters, e.g., /v1/gpay/getByDate?from=2025-02-01&to=2025-02-28
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    if not from_date or not to_date:
        return jsonify({"error": "Please provide both 'from' and 'to' dates"}), 400

    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        query = """
            SELECT * FROM bank_transactions 
            WHERE transaction_date BETWEEN %s AND %s
        """
        cursor.execute(query, (from_date, to_date))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/deleteById/<bank_id>', methods=['DELETE'])
def delete_transaction(bank_id):
    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        query = "DELETE FROM bank_transactions WHERE bank_id = %s"
        cursor.execute(query, (bank_id,))
        conn.commit()
        return jsonify({"message": "Transaction deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/updateById/<bank_id>', methods=['PUT'])
def update_transaction(bank_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        # As an example, we update bank_name and cust_amt. Add other fields as required.
        update_query = """
            UPDATE bank_transactions 
            SET bank_name = %s, cust_amt = %s 
            WHERE bank_id = %s
        """
        params = (
            data.get('bank_name'),
            data.get('cust_amt'),
            bank_id
        )
        cursor.execute(update_query, params)
        conn.commit()
        return jsonify({"message": "Transaction updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@routes.route('/v1/gpay/getByMonth/<month>', methods=['GET'])
def get_transactions_by_month(month):
    """
    Retrieve transactions for a given month.
    Accepts month as either 'MM' (e.g., '02') or 'YYYY-MM' (e.g., '2025-02').
    """
    conn = get_snowflake_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE BANKING_DB")
        cursor.execute("USE SCHEMA BANK")
        # Extract month from the transaction_date using TO_CHAR.
        query = """
            SELECT * FROM bank_transactions 
            WHERE TO_CHAR(transaction_date, 'MM') = %s
        """
        
        month_str = month.split('-')[-1] if '-' in month else month
        cursor.execute(query, (month_str,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
