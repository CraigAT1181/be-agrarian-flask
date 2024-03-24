from datetime import datetime
import psycopg2
import logging

def verify_token(token, verification_type, connection):
    try:
        query = """
        SELECT * from verifications
        WHERE token = %s
        AND verification_type = %s;
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (token, verification_type,))
                token_info = cursor.fetchone()

            if not token_info:
                return None
            
            user_id = token_info[1]
            expires_at = token_info[5]

            if datetime.utcnow() > expires_at:
                return None
            
            return {
                'user_id': user_id,
                'expires_at': expires_at
            }
    
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        logging.error(f"Database error occurred: {e}")
        return None

    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        return None
