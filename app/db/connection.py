import psycopg_pool

from contextlib import contextmanager

# Database configuration
DB_CONFIG = "dbname=hackcamp user=postgres password=postgres host=localhost port=5432"

# Initialize a connection pool
try:
    connection_pool = psycopg_pool.ConnectionPool(
        DB_CONFIG,
        min_size=1,  # Minimum number of connections
        max_size=50,  # Max connections
    )
    if connection_pool:
        print("Connection pool created successfully.")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    raise


def db_connection():
    """
    Context manager to get a database connection from the pool.
    Automatically closes and returns the connection to the pool.
    """
    return connection_pool.connection()
