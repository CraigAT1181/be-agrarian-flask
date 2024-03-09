from flask import jsonify

def fetch_comments_by_blog_id(blog_id, connection):
    try:
        if not blog_id:
            return jsonify({"message": "No blog_id received."}), 400

        query = """
        SELECT c.comment_id, c.blog_id, c.user_id, u.username, c.comment, c.date_posted
        FROM comments c
        JOIN users u ON u.user_id = c.user_id
        WHERE c.blog_id = %s
        ORDER BY c.date_posted DESC;
        """
        
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (blog_id,))
            comments = cursor.fetchall()
            result = []
            for comment in comments:
                result.append({
                    "comment_id": comment[0],
                    "blog_id": comment[1],
                    "user_id": comment[2],
                    "username": comment[3],
                    "comment": comment[4],
                    "date_posted": comment[5]
                })
                
            return jsonify({"comments": result}), 200
    except Exception as e:
        # Log the error for debugging
        print("Error:", e)
        # Return a meaningful error message with status code 500
        return jsonify({"message": "Unable to process this request due to a server error."}), 500
