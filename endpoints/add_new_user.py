import re
from flask_bcrypt import Bcrypt

INSERT_USER = "INSERT INTO users (username, email, password, postcode, produce) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"

def add_new_user(data, connection):
    
    required_fields = ["username", "password", "email", "postcode"]

    for field in required_fields:
        if not data.get(field):
            return {
                "message": f"{field} is required.",
                "status": 400
            }

    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    if not re.match(password_pattern, data["password"]):
        return {
            "message": "Ensure your password meets the requirements.",
            "status": 400
        }
            
    email_pattern = r'^\S+@\S+\.\S+$'
    if not re.match(email_pattern, data["email"]):
        return {
            "message": "Your e-mail doesn't look correct, please check it.",
            "status": 400
        }
    
    postcode_pattern = r'^[A-Za-z]{1,2}[0-9Rr][0-9A-Za-z]?\s?[0-9][ABD-HJLNP-UW-Zabd-hjlnp-uw-z]{2}$'
    if not re.match(postcode_pattern, data["postcode"]):
        return {
            "message": "Invalid UK postcode.",
            "status": 400
        }
    
    bcrypt = Bcrypt()

    username = data["username"]
    email = data["email"]
    password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    postcode = data["postcode"]
    produce = []

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(INSERT_USER, (username, email, password, postcode, produce))
                new_user = cursor.fetchone()
                
                return {
                    "message": "New user registered.",
                    "status": 200,
                    "user_id": new_user[0],
                    "username": username,
                    "email": email,
                    "postcode": postcode,
                    "produce": []
                }
                
            except connection.IntegrityError as e:
                error_message = e.args[0]
                if 'email' in error_message:
                    return {
                        "message": "Email already registered.",
                        "status": 409,
                    }
                elif 'username' in error_message:
                    return {
                        "message": "Username already taken.",
                        "status": 409,
                    }
                else:
                    return {
                        "message": "Error occurred while registering user.",
                        "status": 500,  # Internal Server Error
                    }