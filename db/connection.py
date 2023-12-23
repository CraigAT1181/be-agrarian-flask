from psycopg2 import pool
from db.config import load_db_config
import logging

# Load database configuration from database.ini
db_config = load_db_config()

# Create a database connection pool
_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    **db_config
)

def get_connection():
    try:    # Get a connection from the pool
        connection = _pool.getconn()

        logging.info("Connection acquired from the pool.")

        # Return the connection
        return connection
    except Exception as e:
        logging.error(f"Error acquiring connection from the pool: {e}")
        raise