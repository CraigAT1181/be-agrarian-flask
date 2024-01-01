

INSERT_USER = "INSERT INTO users (user_name, email, password, postcode, produce) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"

def add_new_user(data, hashed_password, connection):

    user_name = data["user_name"]
    email = data["email"]
    hashed_password
    postcode = data["postcode"]
    produce = []

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(INSERT_USER, (user_name, email, hashed_password, postcode, produce))
                new_user = cursor.fetchone()
                
                return {
                    "message": "New user registered.",
                    "status": 200,
                    "user_id": new_user[0],
                    "user_name": user_name,
                    "email": email,
                    "password": hashed_password,
                    "postcode": postcode,
                    "produce": []
                }
                
            except connection.IntegrityError as e:
                return {
                    "message": "email already registered.",
                    "status": 409,
                }