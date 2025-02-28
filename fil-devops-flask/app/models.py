from datetime import datetime
import snowflake.connector
from app.config import Config
from app.utils import generate_transaction_id


class BankTransaction:
    def __init__(self, bank_id, bank_name, bank_ifs_code, cust_id, cust_name,
                 cust_amt, acct_type, trans_date, trans_id, trans_status):
        self.bank_id = bank_id
        self.bank_name = bank_name
        self.bank_ifs_code = bank_ifs_code
        self.cust_id = cust_id
        self.cust_name = cust_name
        self.cust_amt = cust_amt
        self.acct_type = acct_type
        self.trans_date = trans_date
        self.trans_id = trans_id
        self.trans_status = trans_status

    @staticmethod
    def get_connection():
        return snowflake.connector.connect(
            user=Config.SNOWFLAKE_USER,
            password=Config.SNOWFLAKE_PASSWORD,
            account=Config.SNOWFLAKE_ACCOUNT,
            warehouse=Config.SNOWFLAKE_WAREHOUSE,
            database=Config.SNOWFLAKE_DATABASE,
            schema=Config.SNOWFLAKE_SCHEMA
        )

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM BANK_TRANSACTIONS")
            result = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in result]
        finally:
            conn.close()

    @classmethod
    def get_by_cust_id(cls, cust_id):
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM BANK_TRANSACTIONS WHERE CUST_ID = %s", (cust_id,))
            result = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in result]
        finally:
            conn.close()

    @classmethod
    def get_by_trans_id(cls, trans_id):
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM BANK_TRANSACTIONS WHERE TRANS_ID = %s", (trans_id,))
            result = cursor.fetchone()
            if result:
                return dict(zip([col[0] for col in cursor.description], result))
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_date(cls, from_date, to_date):
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM BANK_TRANSACTIONS WHERE TRANS_DATE BETWEEN %s AND %s",
                (from_date, to_date)
            )
            result = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in result]
        finally:
            conn.close()

    @classmethod
    def create_transaction(cls, data):
        """Create a new bank transaction"""
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            trans_id = generate_transaction_id()
            cursor.execute("""
                INSERT INTO BANK_TRANSACTIONS (
                    BANK_ID, BANK_NAME, BANK_IFS_CODE, CUST_ID, 
                    CUST_NAME, CUST_AMT, ACCT_TYPE, TRANS_DATE, 
                    TRANS_ID, TRANS_STATUS
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['bank_id'], data['bank_name'], data['bank_ifs_code'],
                data['cust_id'], data['cust_name'], data['cust_amt'],
                data['acct_type'], datetime.now(),
                trans_id, 'SUCCESS'
            ))
            conn.commit()
            return {"trans_id": trans_id, "status": "SUCCESS"}
        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to create transaction: {str(e)}")
        finally:
            conn.close()
