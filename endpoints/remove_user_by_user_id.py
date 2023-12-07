from flask import jsonify
import psycopg2

def remove_user_by_user_id(user_id, connection):

    DELETE_USER_BY_USER_ID = """
    DELETE FROM users WHERE user_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute(DELETE_USER_BY_USER_ID, (user_id,))
                deleted_user = cursor.fetchone()

                if deleted_user is not None:
                    return jsonify({}), 204
                else:
                    return jsonify({'message': f'User with User ID: {user_id} not found.'}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:

        return jsonify({'message': 'Unable to process this request due to a database error'}), 500
    
