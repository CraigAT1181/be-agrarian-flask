from flask import jsonify

def fetch_all_users(connection):
    
    query = """
    SELECT * FROM users;
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        result = []
        for user in users:
            result.append({
                "user_id": user[0],
                "username": user[1],
                "postcode": user[4],
                "produce": user[5]
            })
        return jsonify({"users": result}), 200


            