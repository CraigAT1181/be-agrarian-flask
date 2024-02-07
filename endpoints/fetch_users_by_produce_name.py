from flask import jsonify

def fetch_users_by_produce_name(connection, produce_list):

    if not produce_list:
        return jsonify({"message": "Produce list currently empty."}), 400

    query = """
    SELECT * FROM users
    WHERE ARRAY[%s]::text[] && users.produce::text[];
    """
    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (produce_list,))
        users = cursor.fetchall()
        result = []
        for user in users:
            result.append({
                "user_id": user[0],
                "username": user[1],
                "postcode": user[4],
                "produce": user[5]
            })
        if not result:
            return jsonify({"message": "No one currently has this item available. Perhaps you could grow it!"})
        else:
            return jsonify({"users": result}), 200
