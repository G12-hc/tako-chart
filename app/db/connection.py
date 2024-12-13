import psycopg_pool

# Database configuration
DB_CONFIG = "dbname=hackcamp user=postgres password=postgres host=localhost port=5432"

# Initialize a connection pool
connection_pool = psycopg_pool.AsyncConnectionPool(
    DB_CONFIG,
    min_size=1,  # Minimum number of connections
    max_size=50,  # Max connections
    open=False,
)


def db_connection():
    """
    Context manager to get a database connection from the pool.
    Automatically closes and returns the connection to the pool.
    """
    return connection_pool.connection()


async def open_connection_pool():
    """
    Open the connection pool to the database.
    """
    await connection_pool.open()


async def close_connection_pool():
    """
    Close the connection pool to the database.
    """
    await connection_pool.close()
