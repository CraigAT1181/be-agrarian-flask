import psycopg2
import logging

def add_conversation(user_id, data, connection):
    user1_id = user_id
    user2_id = data["user2_id"]

    # Check if there's an existing conversation with is_deleted = True
    select_conversation = """
    SELECT conversation_id 
    FROM conversations 
    WHERE (user1_id = %s AND user2_id = %s) 
    OR (user1_id = %s AND user2_id = %s)
    AND (user1_is_deleted = TRUE OR user2_is_deleted = TRUE)
    """

    insert_conversation = """
    INSERT INTO conversations
    (user1_id, user2_id)
    VALUES (%s, %s)
    RETURNING *
    """

    update_conversation = """
        UPDATE conversations
        SET 
            user1_is_deleted = CASE 
                                    WHEN user1_id = %s THEN FALSE 
                                    ELSE user1_is_deleted 
                                END,
            user2_is_deleted = CASE 
                                    WHEN user2_id = %s THEN FALSE 
                                    ELSE user2_is_deleted 
                                END
        WHERE conversation_id = %s
        RETURNING *
        """

    try:
        with connection:
            with connection.cursor() as cursor:
                # Check if there's an existing conversation with is_deleted = True
                cursor.execute(select_conversation, (user1_id, user2_id, user2_id, user1_id))
                existing_conversation = cursor.fetchone()

                if existing_conversation:
                    # If existing conversation found, update it
                    cursor.execute(update_conversation, (user_id, user_id, existing_conversation[0]))
                    updated_conversation = cursor.fetchone()

                    return {
                        "response": "Existing conversation updated.",
                        "status": 200,
                        "conversation_id": updated_conversation[0],
                        "user1_id": updated_conversation[1],
                        "user2_id": updated_conversation[2],
                        "user1_is_deleted": updated_conversation[3] if user_id == updated_conversation[1] else False,
                        "user2_is_deleted": updated_conversation[4] if user_id == updated_conversation[2] else False,
                        "created_at": updated_conversation[5]
                    }

                else:
                    # If no existing conversation found, insert a new one
                    cursor.execute(insert_conversation, (user1_id, user2_id))
                    new_conversation = cursor.fetchone()
                    
                    return {
                        "response": "Conversation started.",
                        "status": 200,
                        "conversation_id": new_conversation[0],
                        "user1_id": user1_id,
                        "user2_id": user2_id,
                        "user1_is_deleted": False,
                        "user2_is_deleted": False,
                        "created_at": new_conversation[5]
                    }
                
    except psycopg2.IntegrityError as e:
        return {
            "message": "Conversation already exists.",
            "status": 409,
        }

    except Exception as e:
        # Log unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        return {
            "message": "An unexpected error occurred.",
            "status": 500,
        }
