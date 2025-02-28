from flask import request, jsonify  # Import request and jsonify from flask module
from flask_restful import Resource  # Import Resource class from flask_restful module
from db import get_snowflake_connection  # Import get_snowflake_connection function from db module

# Creating Custom exception classes and using them later in the code
class DatabaseConnectionError(Exception):
    pass
class RecordNotFoundError(Exception):
    pass
class ValidationError(Exception):
    pass
class TransactionError(Exception):
    pass
class DataProcessingError(Exception):
    pass

class PostTransaction(Resource):  
    def post(self):
        try:
            data = request.json  # Get JSON data from the request
            if not data:
                raise ValidationError("Request body is empty")  # Raise validation error if data is empty
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:  
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("""  
                INSERT INTO fil_devops_flask (bankId, bankName, bankIFSCode, custId, custName, custAmt, acctType, transDate, transId, transStatus)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data.get("bankId"), data.get("bankName"), data.get("bankIFSCode"), 
                data.get("custId"), data.get("custName"), data.get("custAmt"), 
                data.get("acctType"), data.get("transDate"), data.get("transId"), data.get("transStatus")
            ))
            conn.commit()  # Commit the transaction
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            return {"message": "Transaction added successfully"}, 201  # Return success message
        except ValidationError as e:
            return {"error": str(e)}, 400  # Return validation error message
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except Exception as e:  
            return {"error": str(e)}, 500  # Return general error message


class GetAllRecords(Resource):  
    def get(self):
        try:
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("SELECT * FROM fil_devops_flask")  # Execute SQL query to select all records
            data = cur.fetchall()  # Fetch all records
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            if not data:
                raise RecordNotFoundError("No records found")  # Raise record not found error if no data is found
            records = [  # Create a list of records
                {
                    "bankId": row[0], "bankName": row[1], "bankIFSCode": row[2],
                    "custId": row[3], "custName": row[4], "custAmt": row[5],
                    "acctType": row[6], "transDate": row[7], "transId": row[8], "transStatus": row[9]
                }
                for row in data
            ]
            return jsonify(records)  # Return the records as JSON
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message


class GetByCustId(Resource):  
    def get(self, custId):
        try:
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("SELECT * FROM fil_devops_flask WHERE custId = %s", (custId,))  # Execute SQL query to select record by customer ID
            data = cur.fetchall()  # Fetch the record
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            if not data:  
                raise RecordNotFoundError(f"Customer ID {custId} not found")  # Raise record not found error if no data is found
            record = data[0]  # Get the first record
            return jsonify({  # Return the record as JSON
                "bankId": record[0], "bankName": record[1], "bankIFSCode": record[2],
                "custId": record[3], "custName": record[4], "custAmt": record[5],
                "acctType": record[6], "transDate": record[7], "transId": record[8], "transStatus": record[9]
            })
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message


class GetByTransId(Resource):
    def get(self, transId):
        try:
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("SELECT * FROM fil_devops_flask WHERE transId = %s", (transId,))  # Execute SQL query to select record by transaction ID
            data = cur.fetchall()  # Fetch the record
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            if not data:
                raise RecordNotFoundError(f"Transaction ID {transId} not found")  # Raise record not found error if no data is found
            records = [  # Create a list of records
                {
                    "bankId": row[0], "bankName": row[1], "bankIFSCode": row[2],
                    "custId": row[3], "custName": row[4], "custAmt": row[5],
                    "acctType": row[6], "transDate": row[7], "transId": row[8], "transStatus": row[9]
                }
                for row in data
            ]
            return jsonify(records)  # Return the records as JSON
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message

class GetByMonth(Resource):
    def get(self, month):
        try:
            if not 1 <= month <= 12:
                raise ValidationError("Invalid month. Please provide a value between 1 and 12.")  # Raise validation error if month is invalid
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            query = """
                SELECT * FROM fil_devops_flask 
                WHERE MONTH(transDate) = %s
            """
            cur.execute(query, (month,))  # Execute SQL query to select records by month
            data = cur.fetchall()  # Fetch the records
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            if not data:
                raise RecordNotFoundError(f"No transactions found for month {month}")  # Raise record not found error if no data is found
            records = [  # Create a list of records
                {
                    "bankId": row[0], "bankName": row[1], "bankIFSCode": row[2],
                    "custId": row[3], "custName": row[4], "custAmt": row[5],
                    "acctType": row[6], "transDate": row[7], "transId": row[8], "transStatus": row[9]
                }
                for row in data
            ]
            return jsonify(records)  # Return the records as JSON
        except ValidationError as e:
            return {"error": str(e)}, 400  # Return validation error message
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message

class GetByDate(Resource):
    def get(self, from_date, to_date):
        try:
            if not from_date or not to_date:
                raise ValidationError("Both from_date and to_date are required")  # Raise validation error if dates are missing
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            query = """
                SELECT * FROM fil_devops_flask 
                WHERE transDate BETWEEN %s AND %s
            """
            cur.execute(query, (from_date, to_date))  # Execute SQL query to select records by date range
            data = cur.fetchall()  # Fetch the records
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            if not data:
                raise RecordNotFoundError(f"No transactions found between {from_date} and {to_date}")  # Raise record not found error if no data is found
            records = [  # Create a list of records
                {
                    "bankId": row[0], "bankName": row[1], "bankIFSCode": row[2],
                    "custId": row[3], "custName": row[4], "custAmt": row[5],
                    "acctType": row[6], "transDate": row[7], "transId": row[8], "transStatus": row[9]
                }
                for row in data
            ]
            return jsonify(records)  # Return the records as JSON
        except ValidationError as e:
            return {"error": str(e)}, 400  # Return validation error message
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message


class DeleteById(Resource):  
    def delete(self, custId):
        try:
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("DELETE FROM fil_devops_flask WHERE custId = %s", (custId,))  # Execute SQL query to delete record by customer ID
            if cur.rowcount == 0:
                raise RecordNotFoundError(f"Customer ID {custId} not found")  # Raise record not found error if no data is found
            conn.commit()  # Commit the transaction
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            return {"message": "Record deleted successfully"}, 200  # Return success message
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message


class UpdateById(Resource):  
    def put(self, custId):
        try:
            data = request.json  # Get JSON data from the request
            if not data or "custName" not in data or "custAmt" not in data or "acctType" not in data:
                raise ValidationError("Missing required fields: custName, custAmt, acctType")  # Raise validation error if required fields are missing
            conn = get_snowflake_connection()  # Get Snowflake database connection
            if conn is None:
                raise DatabaseConnectionError("Failed to connect to Snowflake")  # Raise database connection error if connection fails
            cur = conn.cursor()  # Create a cursor object
            cur.execute("""  
                UPDATE fil_devops_flask SET custName=%s, custAmt=%s, acctType=%s 
                WHERE custId = %s
            """, (data["custName"], data["custAmt"], data["acctType"], custId))  # Execute SQL query to update record by customer ID
            if cur.rowcount == 0:
                raise RecordNotFoundError(f"Customer ID {custId} not found")  # Raise record not found error if no data is found
            conn.commit()  # Commit the transaction
            cur.close()  # Close the cursor
            conn.close()  # Close the connection
            return {"message": "Record updated successfully"}, 200  # Return success message
        except DatabaseConnectionError as e:
            return {"error": str(e)}, 500  # Return database connection error message
        except RecordNotFoundError as e:
            return {"error": str(e)}, 404  # Return record not found error message
        except ValidationError as e:
            return {"error": str(e)}, 400  # Return validation error message
        except Exception as e:
            return {"error": str(e)}, 500  # Return general error message