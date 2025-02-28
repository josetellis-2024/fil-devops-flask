from flask import Flask, request, jsonify
from db import execute_query
from error_handler import handle_exception, NotFoundError, BadRequestError

app = Flask(__name__)

# Register Custom Error Handler
app.register_error_handler(Exception, handle_exception)

# ✅ **Homepage Route**
@app.route("/", methods=["GET"])
def homepage():
    return jsonify({"message": "Welcome to the Flask E2E Banking API!"})


# ✅ **1. Get All Transactions**
@app.route("/v1/gpay/getall", methods=["GET"])
def get_all_transactions():
    try:
        rows = execute_query("SELECT * FROM transactions")
        if not rows:
            raise NotFoundError("No transactions found")
        return jsonify({"transactions": rows})
    except Exception as e:
        return handle_exception(e)


# ✅ **2. Get Transaction by Customer ID**
@app.route("/v1/gpay/getById/<custId>", methods=["GET"])
def get_transaction_by_custId(custId):
    try:
        row = execute_query("SELECT * FROM transactions WHERE custId = %s", (custId,))
        if not row:
            raise NotFoundError(f"No transaction found for custId: {custId}")
        return jsonify({"transaction": row})
    except Exception as e:
        return handle_exception(e)


# ✅ **3. Get Transaction by Transaction ID**
@app.route("/v1/gpay/getBytransId/<transId>", methods=["GET"])
def get_transaction_by_transId(transId):
    try:
        if len(transId) != 12 or not transId.isdigit():
            raise BadRequestError("Transaction ID must be a 12-digit number")
        row = execute_query("SELECT * FROM transactions WHERE transId = %s", (transId,))
        if not row:
            raise NotFoundError(f"No transaction found for transId: {transId}")
        return jsonify({"transaction": row})
    except Exception as e:
        return handle_exception(e)


# ✅ **4. Get Transactions by Date Range**
@app.route("/v1/gpay/getByDate/<from_date>/<to_date>", methods=["GET"])
def get_transactions_by_date(from_date, to_date):
    try:
        rows = execute_query("SELECT * FROM transactions WHERE transDate BETWEEN %s AND %s", (from_date, to_date))
        if not rows:
            raise NotFoundError(f"No transactions found between {from_date} and {to_date}")
        return jsonify({"transactions": rows})
    except Exception as e:
        return handle_exception(e)


# ✅ **5. Get Transactions by Month**
@app.route("/v1/gpay/getByMonth/<month>", methods=["GET"])
def get_transactions_by_month(month):
    try:
        rows = execute_query("SELECT * FROM transactions WHERE MONTH(transDate) = %s", (month,))
        if not rows:
            raise NotFoundError(f"No transactions found for month: {month}")
        return jsonify({"transactions": rows})
    except Exception as e:
        return handle_exception(e)


# ✅ **6. Delete Transaction by ID**
@app.route("/v1/gpay/deleteById/<custId>", methods=["DELETE"])
def delete_transaction_by_id(custId):
    try:
        execute_query("DELETE FROM transactions WHERE custId = %s", (custId,), fetch=False)
        return jsonify({"message": f"Transaction for custId {custId} deleted successfully"})
    except Exception as e:
        return handle_exception(e)


# ✅ **7. Update Transaction by ID**
@app.route("/v1/gpay/updateById/<custId>", methods=["PUT"])
def update_transaction_by_id(custId):
    try:
        data = request.get_json()
        custName = data.get("custName")
        custAmt = data.get("custAmt")
        transStatus = data.get("transStatus")

        if not custName or not custAmt or not transStatus:
            raise BadRequestError("Missing required fields (custName, custAmt, transStatus)")

        execute_query(
            "UPDATE transactions SET custName=%s, custAmt=%s, transStatus=%s WHERE custId=%s",
            (custName, custAmt, transStatus, custId),
            fetch=False
        )
        return jsonify({"message": f"Transaction for custId {custId} updated successfully"})
    except Exception as e:
        return handle_exception(e)


# ✅ **8. Add New Transaction (POST)**
@app.route("/v1/gpay/addTransaction", methods=["POST"])
def add_transaction():
    try:
        data = request.get_json()
        custId = data.get("custId")
        custName = data.get("custName")
        custAmt = data.get("custAmt")
        acctType = data.get("acctType")
        transDate = data.get("transDate")
        transId = data.get("transId")
        transStatus = data.get("transStatus")

        if not all([custId, custName, custAmt, acctType, transDate, transId, transStatus]):
            raise BadRequestError("Missing required transaction fields")

        execute_query(
            "INSERT INTO transactions (custId, custName, custAmt, acctType, transDate, transId, transStatus) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (custId, custName, custAmt, acctType, transDate, transId, transStatus),
            fetch=False
        )
        return jsonify({"message": "Transaction added successfully"}), 201
    except Exception as e:
        return handle_exception(e)


# ✅ **9. Test Route**
@app.route("/v1/gpay/test", methods=["GET"])
def test():
    return jsonify({"message": "API is running successfully!"})


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
