from flask import jsonify

def fetch_conversations_by_user_id(connection, user_id):

    if not user_id:
        return jsonify({"message": "No user_id received."}), 400

    query = """
    SELECT c.conversation_id, c.user1_id AS curr_user, c.user2_id AS other_user, c.created_at
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
                "curr_user": conversation[1],
                "other_user": conversation[2],
                "created_at": conversation[3]
            })
        return jsonify({"conversations": result}), 200