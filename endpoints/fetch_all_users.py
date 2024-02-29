from flask import jsonify

def fetch_all_users(connection):
    try:
        query = """
        SELECT * FROM users;
        """

        with connection.cursor() as cursor:
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
    except Exception as e:
        return jsonify({"message": f"Error fetching users: {str(e)}"}), 500
