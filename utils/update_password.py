import re 
from flask_bcrypt import Bcrypt
import psycopg2
import logging

UPDATE_PASSWORD = """
    UPDATE users SET password = %s
    WHERE user_id = %s;
    """

def update_password(user_id, new_password, connection):
    try:
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(UPDATE_PASSWORD, (hashed_password, user_id))
        
        return {"message": "Password updated successfully."}, 200
            
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        logging.error(f"Database error occurred: {e}")
        return {"message": "Unable to update password due to a database error."}, 500

    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        return {"message": "Failed to update password due to an unexpected error."}, 500