from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

def authenticate_user(connection, data):
    user = data
    
    username = user.get('username')
    password = user.get('password')

    GET_USER = 'SELECT * FROM users WHERE username = %s;'

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER, (username,))
            fetched_user = cursor.fetchone()
    
    if fetched_user is None:
        return jsonify({"loggedIn": False, "message": "User not found"}), 401

    stored_password = fetched_user[3]

    is_hashed = stored_password.startswith("$2b$")

    bcrypt = Bcrypt()

    if is_hashed:
        
        
        if bcrypt.check_password_hash(stored_password, password):

            additional_claims = {
                "user_id": fetched_user[0],
                "username": fetched_user[1],
                "postcode": fetched_user[4],
                "produce": fetched_user[5],
                "email": fetched_user[2],
            }
    
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            return jsonify({
                "loggedIn": True,
                "access_token": access_token}), 200
        else:
            return jsonify({"loggedIn": False, "message": "Invalid password"}), 401
    
    else:

        if stored_password == password:

            additional_claims = {
                "user_id": fetched_user[0],
                "username": fetched_user[1],
                "postcode": fetched_user[4],
                "produce": fetched_user[5],
                "email": fetched_user[2],
            }
    
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            
            return jsonify({
                "loggedIn": True,
                "access_token": access_token}), 200
        
        else:
            return jsonify({"loggedIn": False, "message": "Invalid password"}), 401