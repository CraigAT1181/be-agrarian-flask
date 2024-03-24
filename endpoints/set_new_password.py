from flask import request, jsonify
from utils.verify_token import verify_token
from utils.update_password import update_password
from utils.set_token_to_used import set_token_to_used
import logging

def set_new_password(data, connection):

    try:
        new_password = data.get('new_password')
        token = data.get('token')
        
        token_info = verify_token(token, 'password_reset', connection)
        if not token_info:
            return jsonify({"message": "Invalid or expired token."}), 400
        
        user_id = token_info.get('user_id')

        if not user_id:
            return jsonify({"message": "Invalid token format. No user_id."}), 400
        
        update_password(user_id, new_password, connection)

        set_token_to_used(token, connection)

        return jsonify({"message": "Password reset successfully."}), 200
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500