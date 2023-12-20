from flask import jsonify

def fetch_all_posts(connection):
    
    query = """
    SELECT p.*, u.postcode, u.user_name AS posted_by
    FROM posts p
    JOIN users u ON p.user_id = u.user_id
    ORDER BY p.created_at;
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query)
        posts = cursor.fetchall()
        result = []
        for post in posts:
            result.append({
                "post_id": post["post_id"],
                "user_id": post["user_id"],
                "status": post["status"],
                "type": post["type"],
                "image": post["image"],
                "body": post["body"],
                "created_at": post["created_at"],
                "postcode": post["postcode"],
                "posted_by":  post["posted_by"]
            })
        
        return jsonify({"posts": result}), 200


            