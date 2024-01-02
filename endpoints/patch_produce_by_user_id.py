from flask import jsonify, abort

def patch_produce_by_user_id(connection, user_id, produce):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET produce = %s
                    WHERE user_id = %s
                    RETURNING *;
                    """,
                    (produce, user_id))
                updated_user = cursor.fetchone()

                if updated_user:
                    response_data = {
                        "user_id": updated_user[0],
                        "username": updated_user[1],
                        "email": updated_user[2],
                        "password": updated_user[3],
                        "postcode": updated_user[4],
                        "produce": updated_user[5]
                    }
                    return jsonify(response_data), 200
                else:                   
                    abort(404, description="User not found")

    except Exception as e:
        
        print(f"Error updating user: {e}")
        abort(500, description="Internal Server Error")
