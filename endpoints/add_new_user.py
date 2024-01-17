import re 

INSERT_USER = "INSERT INTO users (username, email, password, postcode, produce) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"

def add_new_user(data, hashed_password, connection):
    
    required_fields = ["username", "password", "email", "postcode"]

    for field in required_fields:
        if not data.get(field):
            return {
                "message": f"{field} is required.",
                "status": 400
            }
            
    email_pattern = r'^\S+@\S+\.\S+$'
    if not re.match(email_pattern, data["email"]):
        return {
            "message": "Your e-mail doesn't look correct, please check it.",
            "status": 400
        }

    username = data["username"]
    email = data["email"]
    password = hashed_password
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
                    "password": password,
                    "postcode": postcode,
                    "produce": []
                }
                
            except connection.IntegrityError as e:
                return {
                    "message": "Email already registered.",
                    "status": 409,
                }