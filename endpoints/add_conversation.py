import psycopg2

def add_conversation(user_id, data, connection):
    user1_id = user_id
    user2_id = data["user2_id"]

    insert_conversation = """
    INSERT INTO CONVERSATIONS
    (user1_id, user2_id)
    VALUES (%s, %s)
    RETURNING *
    """

    with connection:
        with connection.cursor() as cursor:
            try:
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