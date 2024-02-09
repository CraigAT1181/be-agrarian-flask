from psycopg2 import pool
from db.config import load_db_config
import logging

db_config = load_db_config()
print(db_config, "DB CONFIG")
_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    **db_config
)

def get_connection():
    try:
        connection = _pool.getconn()

        logging.info("Connection acquired from the pool.")

        print("RETURNING CONNECTION")
        return connection
    
    except Exception as e:
        logging.error(f"Error acquiring connection from the pool: {e}")
        raise