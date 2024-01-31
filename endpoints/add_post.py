def add_new_post(data, user_id, connection):
    user_id = user_id,

    if "status" not in data or not data["status"] or "type" not in data or not data["type"]:
         raise ValueError("Ensure you've selected a Status and a Type (e.g. 'Wanted' 'Seeds')")

    status = data["status"]
    type = data["type"]
    item = data["item"]
    image = data["image"]
    body = data["body"]

    insert_post = """
    INSERT INTO POSTS
    (user_id, status, type, item, image, body)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *
    """

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_post, (user_id, status, type, item, image, body))
                new_post = cursor.fetchone()
                
                return {
                    "message": "Post created.",
                    "status": 200,
                    "post_id": new_post[0],
                    "user_id": user_id,
                    "status": status,
                    "type": type,
                    "item": item,
                    "image": image,
                    "body": body,
                    "created_at": new_post[7]
                }
                
            except connection.IntegrityError as e:
                return {
                    "message": "Post already created.",
                    "status": 409,
                }