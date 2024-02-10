from flask import jsonify
import psycopg2

def remove_conversation_by_conversation_id(data, conversation_id, connection):

    user_id = data["user_id"]

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

        return jsonify({'message': 'Unable to process this request due to a database error'}), 500
    
