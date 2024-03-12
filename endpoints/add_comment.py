import psycopg2

def add_comment(blog_id, data, connection):
    
    user_id = data.get("user_id")
    comment = data.get("comment")
    parent_comment_id = data.get("parent_comment_id")

    insert_comment = """
    INSERT INTO COMMENTS
    (blog_id, user_id, comment, parent_comment_id)
    VALUES (%s, %s, %s, %s)
    RETURNING *
    """

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_comment, (blog_id, user_id, comment, parent_comment_id))
                new_comment = cursor.fetchone()
                
                return {
                    "response": "Comment posted.",
                    "status": 200,
                    "comment_id": new_comment[0],
                    "blog_id": new_comment[1],
                    "user_id": new_comment[2],
                    "comment": new_comment[3],
                    "parent_comment_id": new_comment[4],
                    "date_posted": new_comment[5]
                }
                
            except psycopg2.IntegrityError as e:
                return {
                    "message": "Comment already exists.",
                    "status": 409,
                }
    