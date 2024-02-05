import re 
from flask_bcrypt import Bcrypt

UPDATE_PASSWORD = """
    UPDATE users SET password = %s
    WHERE user_id = %s;
    """

def update_password(user_id, new_password, connection):

    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(UPDATE_PASSWORD, (hashed_password, user_id))
            
            except Exception as e:
                print(f"Error updating password: {e}")
                raise
