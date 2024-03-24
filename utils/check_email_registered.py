import psycopg2
import logging

def check_email_registered(email, connection):
    query = """
    SELECT email FROM users WHERE email = %s;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                is_registered = cursor.fetchone()
                return bool(is_registered)
            
    except psycopg2.Error as e:
        logging.error(f"Database error occurred: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False
