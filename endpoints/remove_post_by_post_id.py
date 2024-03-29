from flask import jsonify
import psycopg2
import logging

def remove_post_by_post_id(post_id, connection):

    delete_post = """
    DELETE FROM posts
    WHERE post_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(delete_post, (post_id,))
                deleted_post = cursor.fetchone()

                if deleted_post is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': 'Post not found.'}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        logging.error(f"Database error occurred: {e}")
        return jsonify({'message': 'Unable to process this request due to a database error'}), 500

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({'message': 'An unexpected error occurred'}), 500