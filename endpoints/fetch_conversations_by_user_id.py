from flask import jsonify
import logging
import psycopg2

def fetch_conversations_by_user_id(connection, user_id):

    try:
        if not user_id:
            return jsonify({"message": "No user_id received."}), 400

        query = """
            SELECT c.conversation_id, 
                c.user1_id AS user1_id, 
                u1.username AS user1_username,
                c.user2_id AS user2_id, 
                u2.username AS user2_username,
                c.user1_is_deleted,
                c.user2_is_deleted,
                c.created_at
            FROM conversations c
            JOIN users u1 ON c.user1_id = u1.user_id
            JOIN users u2 ON c.user2_id = u2.user_id
            WHERE ((u1.user_id = %s AND c.user1_is_deleted = FALSE)
            OR (u2.user_id = %s AND c.user2_is_deleted = FALSE))
            AND (
                c.user1_id = %s
                OR EXISTS (
                    SELECT 1 FROM messages m
                    WHERE m.conversation_id = c.conversation_id
                )
            )
            ORDER BY c.created_at DESC;
        """
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, user_id, user_id))
                conversations = cursor.fetchall()
                result = []
                for conversation in conversations:
                    result.append({
                        "conversation_id": conversation[0],
                        "user1_id": conversation[1],
                        "user1_username": conversation[2],
                        "user2_id": conversation[3],
                        "user2_username": conversation[4],
                        "user1_is_deleted": conversation[5],
                        "user2_is_deleted": conversation[6],
                        "created_at": conversation[7]
                    })
                    
                return jsonify({"conversations": result}), 200
        
    except psycopg2.Error as e:
        logging.error(f"Database error occurred: {e}")
        return jsonify({"message": "Database error occurred."}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500