from flask import jsonify

def fetch_blogs_by_user_id(user_id, connection):
    if not user_id:
        return jsonify({"message": "No user_id received."}), 400

    query = """
    SELECT b.blog_id, b.title, b.author_id, u.username, b.content, b.tags, 
           b.date_published, b.image_url  
    FROM blogs b
    JOIN users u ON u.user_id = b.author_id
    WHERE u.user_id = %s;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            blogs = cursor.fetchall()

            result = []
            for blog in blogs:
                result.append({
                    "blog_id": blog[0],
                    "title": blog[1],
                    "author_id": blog[2],
                    "username": blog[3],
                    "content": blog[4],
                    "tags": blog[5],
                    "date_published": blog[6],
                    "image_url": blog[7]
                })
            
            return jsonify({"blogs": result}), 200
        
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
