from io import BytesIO
from PIL import Image
from psycopg2 import IntegrityError
from utils.cloud_authentication import cloud_authentication

def add_blog(image, title, author_id, content, tags, connection):
    try:
        # Check if title and content are provided
        if not title or not content:
            raise ValueError("Blog must contain a title and content.")

        # Set image to None if not provided
        if image is None:
            image_url = None
        else:
            # Determine content type based on file extension
            content_type = "image/jpeg" if image.filename.lower().endswith(".jpeg") or image.filename.lower().endswith(".jpg") else "image/png"

            client = cloud_authentication()
            bucket_name = "cookingpot.live"
            blob_name = f"/images/blogs/{title}.{content_type.split('/')[-1]}"
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Read image data into BytesIO object
            image_data = BytesIO(image.read())
            # Open image using PIL to ensure valid image data
            with Image.open(image_data) as img:
                # Convert to JPEG format if PNG image is uploaded
                if content_type == "image/png":
                    img = img.convert("RGB")
                # Save image data to BytesIO buffer
                img_data_buffer = BytesIO()
                img.save(img_data_buffer, format="JPEG" if content_type == "image/jpeg" else "PNG")
                # Reset the BytesIO buffer's position to the start
                img_data_buffer.seek(0)

            blob.upload_from_string(img_data_buffer.getvalue(), content_type=content_type)
            image_url = blob.public_url

        # Insert the blog into the database
        insert_blog = """
        INSERT INTO BLOGS
        (title, author_id, content, tags, likes, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(insert_blog, (title, author_id, content, tags, 0, image_url))
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
    except ValueError as e:
        return {
            "message": str(e),
            "status": 400,
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
