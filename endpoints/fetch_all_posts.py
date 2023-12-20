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
                "type": post[3],
                "image": post[4],
                "body": post[5],
                "created_at": post[6],
                "postcode": post[7],
                "posted_by":  post[8]
            })
        
        return jsonify({"posts": result}), 200


            