from flask import jsonify

def fetch_conversations_by_user_id(connection, user_id):

    if not user_id:
        return jsonify({"message": "No user_id received."}), 400

    query = """
    SELECT c.conversation_id, u.user_name AS partner_name, c.created_at
    FROM conversations c
    JOIN users u ON (c.user1_id = u.user_id OR c.user2_id = u.user_id)
    WHERE u.user_id = %s;

    """
    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id))
        conversations = cursor.fetchall()
        result = []
        for conversation in conversations:
            result.append({
                "conversation_id": conversation[0],
                "partner_name": conversation[1],
                "created_at": conversation[2]
            })
        return jsonify({"conversations": result}), 200