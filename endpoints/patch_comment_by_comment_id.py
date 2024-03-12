import psycopg2

def patch_comment_by_comment_id(blog_id, comment_id, data, connection):
    comment = data.get("comment")

    patch_comment = """
    UPDATE comments
    SET comment = %s
    WHERE comment_id = %s
    AND blog_id = %s
    RETURNING *
    """

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(patch_comment, (comment, comment_id, blog_id))
                patched_comment = cursor.fetchone()

                if patched_comment:
                    return format_response("Comment edited.", 200, patched_comment)
                else:
                    return format_response("Comment not found.", 404)
            except psycopg2.Error as e:
                return format_response("Database error: " + str(e), 500)

def format_response(message, status, patched_comment=None):
    response = {
        "message": message,
        "status": status,
    }
    if patched_comment:
        response.update({
            "comment_id": patched_comment[0],
            "blog_id": patched_comment[1],
            "user_id": patched_comment[2],
            "comment": patched_comment[3],
            "parent_comment_id": patched_comment[4],
            "date_posted": patched_comment[5],
        })
    return response
