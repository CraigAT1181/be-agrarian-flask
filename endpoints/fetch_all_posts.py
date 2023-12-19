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
                "post_id": post[0],
                "user_id": post[1],
                "status": post[2],
                "type": post[4],
                "image": post[5],
                "body": post[6],
                "created_at": post[7],
                "postcode": post[8],
                "posted_by":  post[9]
            })
        
        return jsonify({"posts": result}), 200


            