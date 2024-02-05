from flask import request, jsonify
from utils.verify_token import verify_token
from utils.update_password import update_password
from utils.set_token_to_used import set_token_to_used

def set_new_password(data, connection):

    new_password = data['new_password']
    token = data['token']
    
    if not verify_token(token, 'password_reset', connection):
        return jsonify({"message": "Invalid or expired token."}), 400
    
    user_id = verify_token(token, 'password_reset', connection)['user_id']

    update_password(user_id, new_password, connection)

    set_token_to_used(token, connection)

    return jsonify({"message": "Password reset successful."}), 200
    