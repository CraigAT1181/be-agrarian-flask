from psycopg2 import IntegrityError

def add_blog(data, connection):
    
    if "title" not in data or not data["title"] or "content" not in data or not data["content"]:
         raise ValueError("Blogs must have a title and some content.")

    title = data["title"]
    author_id = data["author_id"]
    content = data["content"]
    tags = data["tags"]
    likes = 0
    image_url = data["image_url"]    

    insert_blog = """
    INSERT INTO BLOGS
    (title, author_id, content, tags, likes, image_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *
    """
    
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_blog, (title, author_id, content, tags, likes, image_url))
                new_blog = cursor.fetchone()
                
                return {
                    "message": "Blog created.",
                    "status": 200,
                    "blog_id": new_blog[0],
                    "title": new_blog[1],
                    "author_id": author_id,
                    "content": new_blog[3],
                    "tags": new_blog[4],
                    "date_published": new_blog[5],
                    "likes": new_blog[6],
                    "image_url": new_blog[7]
                }
            except IntegrityError as e:
                # Check the specific error message to determine the cause of the integrity error
                if "duplicate key value violates unique constraint" in str(e):
                    return {
                        "message": "Blog with the same title already exists.",
                        "status": 409,
                    }
                else:
                    return {
                        "message": "An error occurred while creating the blog.",
                        "status": 500,
                    }
            except Exception as e:
                # Handle unexpected exceptions
                return {
                    "message": "An unexpected error occurred.",
                    "status": 500,
                }
