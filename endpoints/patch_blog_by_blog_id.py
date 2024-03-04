from flask import jsonify
import psycopg2

def patch_blog_by_blog_id(data, blog_id, connection):
    if not blog_id:
        return jsonify({"message": "No blog_id received."}), 400
    
    elif not data.get("author_id"):
        return jsonify({"message": "No user_id received."}), 400

    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")
    image_url = data.get("image_url")
    author_id = data.get("author_id")

    patch_blog = """
    UPDATE blogs
    SET title = %s,
        content = %s,
        tags = %s,
        image_url = %s
    WHERE blog_id = %s
    AND author_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(patch_blog, (title, content, tags, image_url, blog_id, author_id))
                updated_blog = cursor.fetchone()

                if updated_blog is not None:
                    return jsonify({"message": "Blog updated successfully.", "blog": updated_blog}), 200
                else:
                    return jsonify({"message": "Blog not found."}), 404
                
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        print("Database error:", e)
        return jsonify({"message": "Unable to process this request due to a database error"}), 500
