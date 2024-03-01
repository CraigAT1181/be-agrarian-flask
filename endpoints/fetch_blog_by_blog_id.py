from flask import jsonify

def fetch_blog_by_blog_id(blog_id, connection):
    if not blog_id:
        return jsonify({"message": "No blog_id received."}), 400

    query = """
    SELECT b.blog_id, b.title, u.username, b.content, b.tags, 
           b.date_published, b.image_url  
    FROM blogs b
    JOIN users u ON u.user_id = b.author_id
    WHERE blog_id = %s;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (blog_id,))
            blog = cursor.fetchone()
            if blog:
                return jsonify({
                    "blog_id": blog[0],
                    "title": blog[1],
                    "username": blog[2],
                    "content": blog[3],
                    "tags": blog[4],
                    "date_published": blog[5],
                    "image_url": blog[6]
                })
            else:
                return jsonify({"message": "Blog not found."}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
