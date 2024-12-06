import psycopg
import psycopg_pool

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
        connection = psycopg.connect(
            dbname="hackcamp",  # Correct parameter format
            user="postgres",  # Correct parameter format
            password="postgres",  # Correct parameter format
            host="localhost",  # Correct parameter format
            port="5432",  # Correct parameter format
        )
        print("Database connection established.")
    except Exception as e:
        print(f"Error while connecting to the database: {e}")

    return None  # Return None as specified
