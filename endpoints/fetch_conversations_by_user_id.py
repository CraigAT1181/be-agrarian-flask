from flask import jsonify

def fetch_conversations_by_user_id(connection, user_id):

    if not user_id:
        return jsonify({"message": "No user_id received."}), 400

    query = """
    SELECT * FROM conversations
    WHERE sender_id = %s
    OR recipient_id = %s;
    """
    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, user_id,))
        conversations = cursor.fetchall()
        result = []
        for conversation in conversations:
            result.append({
                "conversation_id": conversation[0],
                "sender_id": conversation[1],
                "recipient_id": conversation[2],
                "body": conversation[3],
                "created_at": conversation[4]
            })
        print(result)
        return jsonify({"conversations": result}), 200