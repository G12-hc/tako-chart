import psycopg2

try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        database="HackCamp",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"  # Default PostgreSQL port
    )
    print("Database connected successfully")

    # Create a cursor object
    cur = conn.cursor()

    # Example: Execute a query
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("PostgresSQL version:", db_version)

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print("An error occurred:", e)

