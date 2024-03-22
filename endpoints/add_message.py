import psycopg2
import logging

def add_message(data, conversation_id, connection):
    sender_id = data.get("sender_id")
    message = data.get("message")

    insert_message = """
    INSERT INTO MESSAGES
    (conversation_id, sender_id, message)
    VALUES (%s, %s, %s)
    RETURNING *
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(insert_message, (conversation_id, sender_id, message))
                new_message = cursor.fetchone()
                
                return {
                    "response": "Message sent.",
                    "status": 200,
                    "message_id": new_message[0],
                    "conversation_id": conversation_id,
                    "sender_id": sender_id,
                    "message": message,
                    "created_at": new_message[4]
                }
                
    except psycopg2.IntegrityError as e:
        # Log specific integrity errors
        logging.error(f"IntegrityError occurred while adding message: {e}")
        return {
            "message": "Message already sent.",
            "status": 409,
        }
    
    except Exception as e:
        # Log unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        return {
            "message": "An unexpected error occurred.",
            "status": 500,
        }
