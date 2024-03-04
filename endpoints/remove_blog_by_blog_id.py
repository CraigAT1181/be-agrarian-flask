from flask import jsonify
import psycopg2

def remove_blog_by_blog_id(blog_id, connection):

    delete_blog = """
    DELETE FROM blogs
    WHERE blog_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(delete_blog, (blog_id,))
                deleted_blog = cursor.fetchone()

                if deleted_blog is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': 'Blog not found.'}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:

        return jsonify({'message': 'Unable to process this request due to a database error'}), 500
    
