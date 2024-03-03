from flask import jsonify

def fetch_comments_by_blog_id(blog_id, connection):

    if not blog_id:
        return jsonify({"message": "No blog_id received."}), 400

    query = """
    SELECT c.comment_id, c.blog_id, u.username, c.comment, c.date_posted
    FROM comments c
    JOIN users u ON u.user_id = c.user_id
    WHERE c.blog_id = %s
    ORDER BY c.date_posted;
    """
    
    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (blog_id))
        comments = cursor.fetchall()
        print(comments)
        result = []
        for comment in comments:
            result.append({
                "comment_id": comment[0],
                "blog_id": comment[1],
                "username": comment[2],
                "comment": comment[3],
                "date_posted": comment[4]
            })
            
        return jsonify({"comments": result}), 200