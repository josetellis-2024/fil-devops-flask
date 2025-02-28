from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'TRANSACTIONS'  # Ensure table name matches Snowflake

    id = db.Column(db.Integer, primary_key=True)
    bankId = db.Column("BANKID", db.String(50), nullable=False)
    bankName = db.Column("BANKNAME", db.String(100), nullable=False)
    bankIFSCode = db.Column("BANKIFSCODE", db.String(20), nullable=False)
    custId = db.Column("CUSTID", db.String(50), nullable=False)
    custName = db.Column("CUSTNAME", db.String(100), nullable=False)
    custAmt = db.Column("CUSTAMT", db.Float, nullable=False)
    acctType = db.Column("ACCTTYPE", db.String(20), nullable=False)
    transDate = db.Column("TRANSDATE", db.String(20), nullable=False)
    transId = db.Column("TRANSID", db.String(12), unique=True, nullable=False)
    transStatus = db.Column("TRANSSTATUS", db.String(50), nullable=False)
