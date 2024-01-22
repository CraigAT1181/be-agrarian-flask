from flask import jsonify
import psycopg2

def remove_conversation_by_conversation_id(conversation_id, connection):

    delete_conversation = """
    DELETE FROM conversations
    WHERE conversation_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(delete_conversation, (conversation_id,))
                deleted_conversation = cursor.fetchone()

                if deleted_conversation is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': 'Conversation not found.'}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:

        return jsonify({'message': 'Unable to process this request due to a database error'}), 500
    
