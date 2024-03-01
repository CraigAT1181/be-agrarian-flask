from flask import jsonify

def fetch_blog_by_blog_id(blog_id, connection):
    if not blog_id:
        return jsonify({"message": "No blog_id received."}), 400

    query = """
    SELECT b.blog_id, b.title, b.author_id, u.username, b.content, b.tags, 
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
                    "author_id": blog[2],
                    "username": blog[3],
                    "content": blog[4],
                    "tags": blog[5],
                    "date_published": blog[6],
                    "image_url": blog[7]
                })
            else:
                return jsonify({"message": "Blog not found."}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
