import snowflake.connector

try:
    conn = snowflake.connector.connect(
        user="lakshay",
        password="LakshayAgarwal6",
        account="gc39555.ap-southeast-1"
    )
    print("Connected to Snowflake successfully!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")