from flask import jsonify
import logging
import psycopg2

def fetch_comments_by_blog_id(blog_id, connection):
    
    try:
        if not blog_id:
            return jsonify({"message": "No blog_id received."}), 400

        query = """
            SELECT
                c.comment_id,
                c.comment,
                c.user_id,
                u.username,
                c.date_posted,
                o.comment_id AS parent_comment_id,
                o.comment AS parent_comment,
                o.user_id AS parent_user_id,
                s.username AS parent_username,
                o.date_posted AS parent_date_posted
            FROM
                comments c
            JOIN
                users u ON u.user_id = c.user_id
            LEFT JOIN
                comments o ON c.parent_comment_id = o.comment_id
            LEFT JOIN
                users s ON s.user_id = o.user_id
            WHERE
                c.blog_id = %s
            ORDER BY
                c.date_posted DESC,
                o.date_posted DESC;
        """
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (blog_id,))
                comments = cursor.fetchall()
                result = []
                for comment in comments:
                    parent_comment_id = comment[5]
                    if parent_comment_id is None:
                        # Top-level comment
                        parent_comment = None
                        parent_user_id = None
                        parent_username = None
                        parent_date_posted = None
                    else:
                        # Reply to another comment
                        parent_comment = comment[6]
                        parent_user_id = comment[7]
                        parent_username = comment[8]
                        parent_date_posted = comment[9]
                    
                    result.append({
                        "comment_id": comment[0],
                        "comment": comment[1],
                        "user_id": comment[2],
                        "username": comment[3],
                        "date_posted": comment[4],
                        "parent_comment_id": parent_comment_id,
                        "parent_comment": parent_comment,
                        "parent_user_id": parent_user_id,
                        "parent_username": parent_username,
                        "parent_date_posted": parent_date_posted
                    })

                return jsonify({"comments": result}), 200
            
    except psycopg2.Error as e:
        logging.error(f"Database error occurred: {e}")
        return jsonify({"message": "Database error occurred."}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500