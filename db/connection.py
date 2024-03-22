from psycopg2 import pool
from db.config import load_db_config
import logging

db_config = load_db_config()

try:
    _pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        **db_config
    )
    logging.info("Database connection pool initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing database connection pool: {e}")
    raise

def get_connection():
    connection = None
    try:
        connection = _pool.getconn()
        logging.info("Connection acquired from the pool.")
        return connection
    except Exception as e:
        logging.error(f"Error acquiring connection from the pool: {e}")
        raise
    finally:
        # Ensure that the connection is returned to the pool, even if an exception occurs
        if connection:
            _pool.putconn(connection)
