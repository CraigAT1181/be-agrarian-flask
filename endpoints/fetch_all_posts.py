from flask import jsonify, request

def fetch_all_posts(connection):

    search_query = request.args.get('item')

    if search_query:
            query = """
            SELECT p.post_id, p.user_id, p.status, p.item, p.type, p.image, p.body, p.created_at, u.postcode, u.username AS posted_by
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.body ILIKE %s
            ORDER BY p.created_at DESC;
            """
    else:
        query = """
        SELECT p.post_id, p.user_id, p.status, p.item, p.type, p.image, p.body, p.created_at, u.postcode, u.username AS posted_by
        FROM posts p
        JOIN users u ON p.user_id = u.user_id
        ORDER BY p.created_at DESC;
        """

    with connection:
        cursor = connection.cursor()
        
        if search_query:
            cursor.execute(query, ('%' + search_query + '%',))

            posts = cursor.fetchall()

            if not posts:
                 return {"message": "Sorry, we couldn't find what you were looking for."}
        
            result = []
            for post in posts:
                result.append({
                    "post_id": post[0],
                    "user_id": post[1],
                    "status": post[2],
                    "item": post[3],
                    "type": post[4],
                    "image": post[5],
                    "body": post[6],
                    "created_at": post[7],
                    "postcode": post[8],
                    "posted_by":  post[9]
                })

            return jsonify({"posts": result}), 200
        
        else:
             cursor.execute(query)
             
        posts = cursor.fetchall()
        result = []
        
        for post in posts:
            result.append({
                "post_id": post[0],
                "user_id": post[1],
                "status": post[2],
                "item": post[3],
                "type": post[4],
                "image": post[5],
                "body": post[6],
                "created_at": post[7],
                "postcode": post[8],
                "posted_by":  post[9]
            })

        return jsonify({"posts": result}), 200


            