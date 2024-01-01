import re 

INSERT_USER = "INSERT INTO users (user_name, email, password, postcode, produce) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"

def add_new_user(data, connection):

    required_fields = ["user_name", "password", "email", "postcode"]

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

    user_name = data["user_name"]
    email = data["email"]
    password = data["password"]
    postcode = data["postcode"]
    produce = []

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(INSERT_USER, (user_name, email, password, postcode, produce))
                new_user = cursor.fetchone()
                
                return {
                    "message": "New user registered.",
                    "status": 200,
                    "user_id": new_user[0],
                    "user_name": user_name,
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