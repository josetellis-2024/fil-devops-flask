from flask import Flask, jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
# from config import Config
from models import db,Transaction
from exceptions import *

app1=Flask(__name__,template_folder='templates')
app1.config['SQLALCHEMY_DATABASE_URI'] = "snowflake://Falafel007:Snowflake__007@tw76742.central-india.azure/fil_db/fil_schema1"
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app1)  # Now bind SQLAlchemy to the Flask app

with app1.app_context():  # Ensure database tables are created within the app context
    db.create_all()


@app1.errorhandler(InvalidTransactionIdError)
def handle_invalid_transaction_id(exc):
    return jsonify({"message":exc.message}),exc.code

@app1.errorhandler(TransactionNotFoundError)
def handle_transaction_not_found(exc):
    return jsonify({"message":exc.message}),exc.code

@app1.errorhandler(InvalidDateError)
def handle_invalid_date(exc):
    return jsonify({"message":exc.message}),exc.code

@app1.errorhandler(InternalServerError)
def handle_internal_server_error(exc):
    return jsonify({"message":exc.message}),exc.code

#Routes

@app1.route('/')
def index():
    return render_template('index.html')

@app1.route('/v1/gpay/addTransaction', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['id', 'bankId', 'bankName', 'bankIFSCode', 'custId', 'custName', 'custAmt', 'acctType', 'transDate', 'transId', 'transStatus']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if transaction ID is valid
        if len(data['transId']) != 12 or not data['transId'].isdigit():
            raise InvalidTransactionIdError()

        # Check if transaction ID already exists
        existing_transaction = Transaction.query.filter_by(transId=data['transId']).first()
        if existing_transaction:
            return jsonify({'message': 'Transaction ID already exists'}), 400

        # Convert transDate to datetime format
        from datetime import datetime
        trans_date = datetime.strptime(data['transDate'], '%Y-%m-%d')

        new_transaction = Transaction(
            id=data["id"],
            bankId=data["bankId"],
            bankName=data["bankName"],
            bankIFSCode=data["bankIFSCode"],
            custId=data["custId"],
            custName=data["custName"],
            custAmt=data["custAmt"],
            acctType=data["acctType"],
            transDate=trans_date,  # Ensure the format matches DB schema
            transId=data["transId"],
            transStatus=data["transStatus"]
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction added successfully'}), 201

    except InvalidTransactionIdError:
        return jsonify({'message': 'Invalid Transaction ID'}), 400
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500



@app1.route('/v1/gpay/getall',methods=['GET'])
def get_all_transactions():
    try:
        transactions = Transaction.query.all()
        return jsonify([{'transId':t.transId, 'custName':t.custName} for t in transactions])
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/getById/<custId>',methods=['GET'])
def get_by_cust_id(custId):
    try:
        transactions=Transaction.query.filter_by(custId=custId).all()
        if not transactions:
            raise TransactionNotFoundError()
        return jsonify([{'transId':t.transId, 'custName':t.custName} for t in transactions])
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/getBytransId/<transId>',methods=['GET'])
def get_by_trans_id(transId):
    try:
        if len(transId)!=12 or not transId.isdigit():
            raise InvalidTransactionIdError()
        transaction=Transaction.query.filter_by(transId=transId).first()
        if not transaction:
            raise TransactionNotFoundError()
        return jsonify({'transId':transaction.transId, 'custName':transaction.custName})
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/getByDate',methods=['GET'])
def get_by_date():
    try:
        from_date=request.args.get('from')
        to_date=request.args.get('to')
        # Validate date format here if necessary
        transactions = Transaction.query.filter(Transaction.transDate>=from_date,Transaction.transDate<=to_date).all()
        return jsonify([{'transId':t.transId, 'custName':t.custName} for t in transactions])
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/deleteById/<transId>', methods=['DELETE'])
def delete_by_id(transId):
    try:
        if len(transId)!=12 or not transId.isdigit():
            raise InvalidTransactionIdError()
        transaction=Transaction.query.filter_by(transId=transId).first()
        if not transaction:
            raise TransactionNotFoundError()
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message':'Transaction deleted successfully'})
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/updateById/<transId>',methods=['PUT'])
def update_by_id(transId):
    try:
        if len(transId)!=12 or not transId.isdigit():
            raise InvalidTransactionIdError()
        transaction=Transaction.query.filter_by(transId=transId).first()
        if not transaction:
            raise TransactionNotFoundError()
        data=request.get_json()
        transaction.custName=data.get('custName',transaction.custName)
        db.session.commit()
        return jsonify({'message':'Transaction updated successfully'})
    except Exception as e:
        raise InternalServerError()

@app1.route('/v1/gpay/getByMonth',methods=['GET'])
def get_by_month():
    try:
        month=request.args.get('month')
        year=request.args.get('year')
        transactions=Transaction.query.filter(Transaction.transDate.strftime('%Y-%m')==f'{year}-{month}').all()
        return jsonify([{'transId':t.transId, 'custName':t.custName} for t in transactions])
    except Exception as e:
        raise InternalServerError()

if __name__ == '__main__':
    app1.run(debug=True)
