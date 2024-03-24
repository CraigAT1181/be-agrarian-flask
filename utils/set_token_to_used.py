import psycopg2
import logging
from flask import jsonify

SET_USED = """
UPDATE verifications SET is_used = 'true'
WHERE token = %s;
"""

def set_token_to_used(token, connection):
    try:
        if not token:
            raise ValueError("No token received.")

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SET_USED, (token,))
        
        return {"message": "Token updated successfully."}, 200
            
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        logging.error(f"Database error occurred: {e}")
        return {"message": "Unable to update token due to a database error."}, 500

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return {"message": str(ve)}, 400

    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        return {"message": "Failed to update token due to an unexpected error."}, 500