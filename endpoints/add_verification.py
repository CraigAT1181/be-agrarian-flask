from datetime import datetime, timedelta
import psycopg2
import logging

def add_verification(email, token, verification_type, connection):

    GET_USER_ID = """
            SELECT user_id FROM users WHERE email = %s;
        """

    CREATE_VERIFICATION = "INSERT INTO verifications (user_id, token, verification_type, expires_at) VALUES (%s, %s, %s, %s) RETURNING *;"

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_USER_ID, (email,))
                fetched_user_id = cursor.fetchone()

                if fetched_user_id is None:
                    return {
                        "message": "User not found.",
                        "status": 404,
                    }

                user_id = fetched_user_id[0]
                expires_at = datetime.utcnow() + timedelta(minutes=60)

                cursor.execute(CREATE_VERIFICATION, (user_id, token, verification_type, expires_at))
                new_entry = cursor.fetchone()
    
                return {
                    "message": "New entry added to verifications.",
                    "verification_id": new_entry[0],
                    "user_id": user_id,
                    "token": token,
                    "verification_type": verification_type,
                    "created_at": new_entry[4],
                    "expires_at": new_entry[5],
                    "is_used": new_entry[6]
                }

    except psycopg2.Error as e:
        logging.error(f"Error occurred during verification creation: {e}")
        return {
            "message": "Error creating verification entry.",
            "status": 500,
        }
