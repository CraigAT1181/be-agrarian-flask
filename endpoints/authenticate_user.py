from flask import request, jsonify

GET_USERS = 'SELECT * FROM users;'

def authenticate_user(connection, data):
    user = data
    
    username = user.get('username')
    password = user.get('password')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USERS)
            users = cursor.fetchall() 

    user_data = {user[1]: {'user_id': user[0], 'password': user[3], 'postcode': user[4], 'produce': user[5], 'email': user[2]} for user in users}
    
    if username not in user_data:
        return jsonify({"loggedIn": False, "message": "User not found"}), 401

    stored_password = user_data[username]['password']
    if password == stored_password:
        return jsonify({"loggedIn": True, "user_name": username, "user_id": user_data[username]['user_id'], "postcode": user_data[username]["postcode"], "produce": user_data[username]["produce"], "email": user_data[username]["email"]}), 200
    else:
        return jsonify({"loggedIn": False, "message": "Invalid password"}), 401