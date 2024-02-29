from flask import jsonify

def fetch_all_blogs(connection):
    try:
        query = """
        SELECT * FROM blogs;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            blogs = cursor.fetchall()
            result = []
            
            for blog in blogs:
                result.append({
                    "blog_id": blog[0],
                    "title": blog[1],
                    "author_id": blog[2],
                    "content": blog[3],
                    "tags": blog[4],
                    "date_published": blog[5],
                    "likes": blog[6],
                    "image_url": blog[7]
                })

            return jsonify({"blogs": result}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching blogs: {str(e)}"}), 500
