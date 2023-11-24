from flask import jsonify

def fetch_users_by_produce_name(connection, produce_name):
    query = """
    SELECT * FROM users
    WHERE %s = ANY(produce);
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (produce_name,))
        users = cursor.fetchall()
        if users:
            result = []
            for user in users:
                result.append({
                    "user_id": user[0],
                    "user_name": user[1],
                    "postcode": user[4],
                    "produce": user[5]
                })
            return jsonify({"users": result}), 200
        else:
            return {"message": f"No one is currently trading {produce_name}"}, 200

            