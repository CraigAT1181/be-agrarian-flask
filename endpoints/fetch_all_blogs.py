from flask import jsonify
import logging

def fetch_all_blogs(connection):
    
    query = """
    SELECT b.blog_id, b.title, b.author_id, u.username, b.content, b.tags, b.date_published, b.image_url  
    FROM blogs b
    JOIN users u ON u.user_id = b.author_id
    ORDER BY b.date_published DESC;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
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
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": f"Error fetching blogs: {str(e)}"}), 500
