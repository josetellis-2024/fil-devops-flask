import snowflake.connector
from error_handler import DatabaseError

# Snowflake Connection Details (DO NOT Hardcode Passwords in Production!)
SNOWFLAKE_CONFIG = {
    "user": "KRIS007",
    "password": "chessChess2*2*",  # Move this to an environment variable
    "account": "LG01426.ap-southeast-1",
    "warehouse": "COMPUTE_WH",
    "database": "FIDELITY_TEST",
    "schema": "MY_SCHEMA",
}

def get_snowflake_connection():
    """Establishes and returns a Snowflake connection."""
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        return conn
    except Exception as e:
        raise DatabaseError(f"Failed to connect to Snowflake: {str(e)}")

def execute_query(query, params=None, fetch=True):
    """Executes a given SQL query with optional parameters."""
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to execute query: {str(e)}")
    finally:
        conn.close()
