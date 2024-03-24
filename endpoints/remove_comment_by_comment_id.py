from flask import jsonify
import psycopg2
import logging

def remove_comment_by_comment_id(blog_id, comment_id, connection):

    delete_comment = """
    DELETE FROM comments
    WHERE comment_id = %s
    AND blog_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(delete_comment, (comment_id, blog_id))
                deleted_comment = cursor.fetchone()

                if deleted_comment is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': 'Comment not found.'}), 404
                
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