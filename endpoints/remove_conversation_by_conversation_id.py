from flask import jsonify
import psycopg2
import logging

def remove_conversation_by_conversation_id(data, conversation_id, connection):

    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "User ID is required."}), 400

    soft_delete_conversation = """
    UPDATE conversations
    SET user1_is_deleted = CASE WHEN user1_id = %s THEN TRUE ELSE user1_is_deleted END,
        user2_is_deleted = CASE WHEN user2_id = %s THEN TRUE ELSE user2_is_deleted END
    WHERE conversation_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(soft_delete_conversation, (user_id, user_id, conversation_id))
                softly_deleted_conversation = cursor.fetchone()

                if softly_deleted_conversation is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': 'Conversation not found.'}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        # Log the database error for debugging
        logging.error(f"Database error occurred: {e}")
        # Return a meaningful error message to the client
        return jsonify({'message': 'Unable to process this request due to a database error'}), 500

    except Exception as e:
        # Log unexpected errors for debugging
        logging.error(f"An unexpected error occurred: {e}")
        # Return a generic error message to the client
        return jsonify({'message': 'An unexpected error occurred'}), 500