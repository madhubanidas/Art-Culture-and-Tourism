from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv()

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse='COMPUTE_WH',
        database='CULTURE_TOURISM_DB',
        schema='PUBLIC'
    )
    return conn
 