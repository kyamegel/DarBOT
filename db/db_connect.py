import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **dbconfig
    )
    print("✅ MySQL connection pool created.")
except mysql.connector.Error as err:
    print(f"❌ MySQL connection error: {err}")

def get_connection():
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"❌ Error getting connection: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
    finally:
        cursor.close()
        conn.close()
