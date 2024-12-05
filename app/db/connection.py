

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Database configuration
DB_CONFIG = {
    "dbname": "HackCamp",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Initialize a connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,  # Minimum number of connections
        maxconn=10,  # Maximum number of connections
        **DB_CONFIG
    )
    if connection_pool:
        print("Connection pool created successfully.")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    raise

def get_db_connection():
    """
    Context manager to get a database connection from the pool.
    Automatically closes and returns the connection to the pool.
    """
    conn = None
    try:
        conn = connection_pool.getconn()  # Get connection from pool
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)  # Return connection to the pool

# Utility function to fetch data from the database
def fetch_all(query, params=None):
    """
    Execute a SELECT query and return all rows.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

# Utility function to fetch a single row
def fetch_one(query, params=None):
    """
    Execute a SELECT query and return a single row.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

# Utility function to execute an INSERT, UPDATE, or DELETE query
def execute_query(query, params=None):
    """
    Execute a query that modifies data (INSERT, UPDATE, DELETE).
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            conn.commit()



# Define a global variable to hold the database connection
connection = None

def initialize_db():
    """
    Initializes the connection to the PostgreSQL database
    This function could be expanded to include connection parameters,
    and error handling.
    """
    global connection
    try:
        # Replace these with your database credentials
        connection = psycopg2.connect(
            dbname="HackCamp",        # Correct parameter format
            user="postgres",          # Correct parameter format
            password="postgres",      # Correct parameter format
            host="localhost",         # Correct parameter format
            port="5432"               # Correct parameter format
        )
        print("Database connection established.")
    except Exception as e:
        print(f"Error while connecting to the database: {e}")

    return None  # Return None as specified

