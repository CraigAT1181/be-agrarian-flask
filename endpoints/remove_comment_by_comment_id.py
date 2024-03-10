from flask import jsonify
import psycopg2

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

        return jsonify({'message': 'Unable to process this request due to a database error'}), 500
    
