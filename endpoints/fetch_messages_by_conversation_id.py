from flask import jsonify
import psycopg2
import logging

def fetch_messages_by_conversation_id(connection, conversation_id):

    if not conversation_id:
        return jsonify({"error": "Conversation ID not found."}), 400

    query = """
    SELECT m.message_id, m.conversation_id, m.sender_id, u.username AS sender_name, m.message, m.created_at
    FROM messages m
    JOIN users u ON m.sender_id = u.user_id
    JOIN conversations c ON m.conversation_id = c.conversation_id
    WHERE m.conversation_id = %s
    ORDER BY m.created_at;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (conversation_id,))
                messages = cursor.fetchall()

                result = []
                for message in messages:
                    result.append({
                        "message_id": message[0],
                        "conversation_id": message[1],
                        "sender_id": message[2],
                        "sender_name": message[3],
                        "message": message[4],
                        "created_at": message[5]
                    })
                
                return jsonify({"messages": result}), 200
    
    except psycopg2.Error as e:
        logging.error(f"Database error occurred: {e}")
        return jsonify({"message": "Database error occurred."}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500