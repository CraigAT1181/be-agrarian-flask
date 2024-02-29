from flask import jsonify

def fetch_all_blogs(connection):
    try:
        query = """
        SELECT b.blog_id, b.title, u.username, b.content, b.tags, b.date_published, b.likes, b.image_url  
        FROM blogs b
        JOIN users u ON u.user_id = b.author_id
        ORDER BY b.date_published DESC;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            blogs = cursor.fetchall()
            result = []
            
            for blog in blogs:
                result.append({
                    "blog_id": blog[0],
                    "title": blog[1],
                    "username": blog[2],
                    "content": blog[3],
                    "tags": blog[4],
                    "date_published": blog[5],
                    "likes": blog[6],
                    "image_url": blog[7]
                })

            return jsonify({"blogs": result}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching blogs: {str(e)}"}), 500
