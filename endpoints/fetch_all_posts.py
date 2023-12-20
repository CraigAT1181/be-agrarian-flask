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
                "post_id": post[3],
                "user_id": post[8],
                "status": post[6],
                "type": post[7],
                "image": post[2],
                "body": post[0],
                "created_at": post[1],
                "postcode": post[4],
                "posted_by":  post[5]
            })
        
        return jsonify({"posts": result}), 200


            