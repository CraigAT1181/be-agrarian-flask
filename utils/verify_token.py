from datetime import datetime

def verify_token(token, verification_type, connection):

    query = """
    SELECT * from verifications
    WHERE token = %s
    AND verification_type = %s;
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (token, verification_type,))
        token_info = cursor.fetchone()

    if not token_info:
        return None
    
    user_id = token_info[1]
    expires_at = token_info[5]

    if datetime.utcnow() > expires_at:
        return None
    
    return {
        'user_id': user_id,
        'expires_at': expires_at
    }