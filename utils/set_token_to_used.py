from flask import jsonify

SET_USED = """
UPDATE verifications SET is_used = 'true'
WHERE token = %s;
"""

def set_token_to_used(token, connection):

    if not token:
        return jsonify({"message":  "No token received."}), 400
    
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(SET_USED, (token,))
            
            except Exception as e:
                print(f"Error updating password: {e}")
                raise
