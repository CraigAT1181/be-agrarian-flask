def add_message(data, conversation_id, connection):
    conversation_id = conversation_id,
    sender_id = data["sender_id"]
    message = data["message"]

    insert_message = """
    INSERT INTO MESSAGES
    (conversation_id, sender_id, message)
    VALUES (%s, %s, %s)
    RETURNING *
    """

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_message, (conversation_id, sender_id, message))
                new_message = cursor.fetchone()
                
                return {
                    "response": "Message sent.",
                    "status": 200,
                    "message_id": new_message[0],
                    "conversation_id": conversation_id[0],
                    "sender_id": sender_id,
                    "message": message,
                    "created_at": new_message[4]
                }
                
            except connection.IntegrityError as e:
                return {
                    "message": "Message already sent.",
                    "status": 409,
                }