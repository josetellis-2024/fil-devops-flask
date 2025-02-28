from flask import Flask, request, jsonify
import snowflake.connector
import re

app = Flask(__name__)

# Snowflake Configuration
SNOWFLAKE_CONFIG = {
    "user": "lakshay",
    "password": "LakshayAgarwal6",
    "account": "gc39555.ap-southeast-1",
    "warehouse": "w1",
    "database": "db1",
    "schema": "s1"
}

# Custom Exception
class BankException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

@app.errorhandler(BankException)
def handle_custom_exception(error):
    response = jsonify({"error": str(error)})
    response.status_code = error.status_code
    return response

# Connect to Snowflake
def get_snowflake_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)

# Bank Model
class Bank:
    def __init__(self, bankId, bankName, bankIFSCode, custId, custName, custAmt, acctType, transDate, transId, transStatus):
        if not re.match(r"^[1-9]\d{11}$", str(transId)):
            raise BankException("Invalid Transaction ID. Must be a 12-digit number greater than 99999999999")
        self.bankId = bankId
        self.bankName = bankName
        self.bankIFSCode = bankIFSCode
        self.custId = custId
        self.custName = custName
        self.custAmt = custAmt
        self.acctType = acctType
        self.transDate = transDate
        self.transId = transId
        self.transStatus = transStatus
        
@app.route("/v1/gpay/post", methods=["POST"])
def create_bank_record():
    try:
        data = request.json
        bank = Bank(**data)  # Validate data
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Bank (bankId, bankName, bankIFSCode, custId, custName, custAmt, acctType, transDate, transId, transStatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (bank.bankId, bank.bankName, bank.bankIFSCode, bank.custId, bank.custName, bank.custAmt, bank.acctType, bank.transDate, bank.transId, bank.transStatus))
        conn.commit()
        conn.close()
        return jsonify({"message": "Record inserted successfully"})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/getall", methods=["GET"])
def get_all():
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank")
        records = cursor.fetchall()
        conn.close()
        return jsonify({"data": records})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/getById/<int:bank_id>", methods=["GET"])
def get_by_id(bank_id):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE bankId = %s", (bank_id,))
        record = cursor.fetchone()
        conn.close()
        if not record:
            raise BankException("Bank ID not found", 404)
        return jsonify({"data": record})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/custId/<int:cust_id>", methods=["GET"])
def get_by_cust_id(cust_id):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE custId = %s", (cust_id,))
        records = cursor.fetchall()
        conn.close()
        return jsonify({"data": records})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/getBytransId/<int:trans_id>", methods=["GET"])
def get_by_trans_id(trans_id):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE transId = %s", (trans_id,))
        record = cursor.fetchone()
        conn.close()
        if not record:
            raise BankException("Transaction ID not found", 404)
        return jsonify({"data": record})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/getByDate/<string:date>", methods=["GET"])
def get_by_date(date):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE transDate = %s", (date,))
        records = cursor.fetchall()
        conn.close()
        return jsonify({"data": records})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/<string:from_date>/<string:to_date>", methods=["GET"])
def get_by_date_range(from_date, to_date):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE transDate BETWEEN %s AND %s", (from_date, to_date))
        records = cursor.fetchall()
        conn.close()
        return jsonify({"data": records})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/deleteById/<int:bank_id>", methods=["DELETE"])
def delete_by_id(bank_id):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bank WHERE bankId = %s", (bank_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Deleted successfully"})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/updateById/<int:bank_id>", methods=["PUT"])
def update_by_id(bank_id):
    try:
        data = request.json
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Bank SET bankName = %s WHERE bankId = %s", (data.get("bankName"), bank_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Updated successfully"})
    except Exception as e:
        raise BankException(str(e))

@app.route("/v1/gpay/getByMonth/<int:month>", methods=["GET"])
def get_by_month(month):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bank WHERE MONTH(transDate) = %s", (month,))
        records = cursor.fetchall()
        conn.close()
        return jsonify({"data": records})
    except Exception as e:
        raise BankException(str(e))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)