from flask import jsonify

def fetch_messages_by_conversation_id(connection, conversation_id):

    if not conversation_id:
        return jsonify({"message": "Conversation ID not found."}), 400

    query = """
    SELECT m.message_id, m.sender_id, u.username AS sender_name, m.message, m.created_at
    FROM messages m
    JOIN users u ON m.sender_id = u.user_id
    WHERE m.conversation_id = %s
    ORDER BY m.created_at;
    """
    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (conversation_id))
        messages = cursor.fetchall()
        result = []
        for message in messages:
            result.append({
                "message_id": message[0],
                "sender_id": message[1],
                "sender_name": message[2],
                "message": message[3],
                "created_at": message[4]
            })
        
        return jsonify({"messages": result}), 200