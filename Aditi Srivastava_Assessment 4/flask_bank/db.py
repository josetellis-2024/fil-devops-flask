import snowflake.connector
from config import SNOWFLAKE_CONFIG

def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        print("Connected to Snowflake successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None
