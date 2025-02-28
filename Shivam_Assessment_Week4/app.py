from flask import Flask, request, jsonify
import snowflake.connector
from custom_exceptions import NotFoundError, ValidationError

app = Flask(__name__)

# Snowflake connection config
def get_db_connection():
    return snowflake.connector.connect(
        user='shivawmm',
        password='Shivamsingh@181002',
        account='zg03012.ap-southeast-1',
        database='DB1',
        schema='PUBLIC'
    )

@app.route("/", methods=["GET"])
def homepage():
    return jsonify({"message": "Welcome to the Flask E2E Banking API!"})

@app.route('/v1/gpay/getall', methods=['GET'])
def get_all():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if not data:
            raise NotFoundError("No transactions found")
        return jsonify({"transactions": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/getById/<custId>', methods=['GET'])
def get_by_id(custId):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE custId = %s", (custId,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if not data:
            raise NotFoundError(f"Customer with ID {custId} not found")
        return jsonify({"transaction": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/getBytransId/<transId>', methods=['GET'])
def get_transaction_by_transId(transId):
    try:
        if len(transId) != 12 or not transId.isdigit():
            raise ValidationError("Transaction ID must be a 12-digit number")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE transId = %s", (transId,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if not data:
            raise NotFoundError(f"No transaction found for transId: {transId}")
        return jsonify({"transaction": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/getByDate/<from_date>/<to_date>', methods=['GET'])
def get_transactions_by_date(from_date, to_date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE transDate BETWEEN %s AND %s", (from_date, to_date))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if not data:
            raise NotFoundError(f"No transactions found between {from_date} and {to_date}")
        return jsonify({"transactions": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/getByMonth/<month>', methods=['GET'])
def get_by_month(month):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE MONTH(transDate) = %s", (month,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if not data:
            raise NotFoundError(f"No transactions found for month: {month}")
        return jsonify({"transactions": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/addTransaction', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        required_fields = ["bankId", "bankName", "bankIFSCode", "custId", "custName", "custAmt", "acctType", "transDate", "transId", "transStatus"]
        if not all(field in data for field in required_fields):
            raise ValidationError("Missing required transaction fields")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Bank (bankId, bankName, bankIFSCode, custId, custName, custAmt, acctType, transDate, transId, transStatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data["bankId"], data["bankName"], data["bankIFSCode"], data["custId"], data["custName"],
             data["custAmt"], data["acctType"], data["transDate"], data["transId"], data["transStatus"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Transaction added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/updateById/<custId>', methods=['PUT'])
def update_transaction(custId):
    try:
        data = request.get_json()
        if not all(key in data for key in ["custName", "custAmt", "acctType", "transStatus"]):
            raise ValidationError("Missing required fields (custName, custAmt, acctType, transStatus)")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Bank
            SET custName = %s, custAmt = %s, acctType = %s, transStatus = %s
            WHERE custId = %s
            """,
            (data["custName"], data["custAmt"], data["acctType"], data["transStatus"], custId)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": f"Transaction for custId {custId} updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/deleteById/<custId>', methods=['DELETE'])
def delete_transaction(custId):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bank WHERE custId = %s", (custId,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": f"Transaction for custId {custId} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/gpay/test', methods=['GET'])
def test():
    return jsonify({"message": "API is running successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
