from flask import jsonify, abort

def patch_produce_by_user_id(connection, user_id, produce):
    try:
        with connection:
            with connection.cursor() as cursor:
                if not produce:  # Check if produce is empty
                    cursor.execute(
                        """
                        UPDATE users
                        SET produce = ARRAY[]::text[]
                        WHERE user_id = %s
                        RETURNING *;
                        """,
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE users
                        SET produce = ARRAY(SELECT DISTINCT UNNEST(%s))
                        WHERE user_id = %s
                        RETURNING *;
                        """,
                        (produce, user_id)
                    )
                updated_user = cursor.fetchone()
                if updated_user:
                    response_data = {
                        "user_id": updated_user[0],
                        "username": updated_user[1],
                        "email": updated_user[2],
                        "postcode": updated_user[4],
                        "produce": updated_user[5]
                    }
                    return jsonify(response_data), 200
                else:
                    abort(404, description="User not found")

    except Exception as e:
        print(f"Error updating user: {e}")
        abort(500, description="Internal Server Error")

