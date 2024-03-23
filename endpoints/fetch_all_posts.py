from flask import jsonify, request
import logging

def fetch_all_posts(connection):

    search_query = request.args.get('item')

    if search_query:
        query = """
        SELECT p.post_id, p.user_id, p.status, p.item, p.type, p.image, p.body, p.created_at, u.postcode, u.username AS posted_by
        FROM posts p
        JOIN users u ON p.user_id = u.user_id
        WHERE p.body ILIKE %s OR p.item ILIKE %s
        ORDER BY p.created_at DESC;
        """
        params = ('%' + search_query + '%', '%' + search_query + '%')
    else:
        query = """
        SELECT p.post_id, p.user_id, p.status, p.item, p.type, p.image, p.body, p.created_at, u.postcode, u.username AS posted_by
        FROM posts p
        JOIN users u ON p.user_id = u.user_id
        ORDER BY p.created_at DESC;
        """
        params = None

    try:
        with connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
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
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": f"Error fetching posts: {str(e)}"}), 500


            