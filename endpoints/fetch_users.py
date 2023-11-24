from flask import jsonify, request

def fetch_users(connection):
    produce = request.args.get("produce")

    query1 = """
    SELECT * FROM users;
    """
    query2 = """
    SELECT * FROM users
    WHERE %s = ANY(produce);
    """

    if not produce:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query1)
            users = cursor.fetchall()
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
        with connection:
            cursor = connection.cursor()
            cursor.execute(query2, (produce,))
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
                return jsonify({"message": f"No one is currently trading {produce}"}), 200


            