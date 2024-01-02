from flask import jsonify

def fetch_conversations_by_user_id(connection, user_id):

    if not user_id:
        return jsonify({"message": "No user_id received."}), 400

    query = """
        SELECT c.conversation_id, 
            c.user1_id AS user1_id, 
            u1.username AS user1_username,
            c.user2_id AS user2_id, 
            u2.username AS user2_username,
            c.created_at
        FROM conversations c
        JOIN users u1 ON c.user1_id = u1.user_id
        JOIN users u2 ON c.user2_id = u2.user_id
        WHERE u1.user_id = %s OR u2.user_id = %s;
    """

    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, user_id))
        conversations = cursor.fetchall()
        result = []
        for conversation in conversations:
            result.append({
                "conversation_id": conversation[0],
                "user1_id": conversation[1],
                "user1_username": conversation[2],
                "user2_id": conversation[3],
                "user2_username": conversation[4],
                "created_at": conversation[5]
            })
        return jsonify({"conversations": result}), 200