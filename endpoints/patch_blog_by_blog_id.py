from flask import jsonify
from io import BytesIO
from PIL import Image
import psycopg2
from utils.cloud_authentication import cloud_authentication

def patch_blog_by_blog_id(blog_id, image, title, author_id, content, tags, connection):
    
    def process_image(image, title):
        print("image:", image)
        if image is None:
            return None
        
        if isinstance(image, str) and image.startswith('https://storage'):
            return image
    
        if hasattr(image, 'read'):
            content_type = "image/jpeg" if image.filename.lower().endswith(".jpeg") or image.filename.lower().endswith(".jpg") else "image/png"

            client = cloud_authentication()
            bucket_name = "cookingpot.live"
            blob_name = f"/images/blogs/{title}.{content_type.split('/')[-1]}"
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)

            image_data = BytesIO(image.read())
        
            with Image.open(image_data) as img:
                if content_type == "image/png":
                    img = img.convert("RGB")
                
                img_data_buffer = BytesIO()
                img.save(img_data_buffer, format="JPEG" if content_type == "image/jpeg" else "PNG")
                img_data_buffer.seek(0)

            blob.upload_from_string(img_data_buffer.getvalue(), content_type=content_type)
            return blob.public_url
    
    try:
        updated_image_url = process_image(image, title)

        patch_blog = """
        UPDATE blogs
        SET image_url = %s, title = %s, content = %s, tags = %s
        WHERE blog_id = %s AND author_id = %s
        RETURNING *;
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(patch_blog, (updated_image_url, title, content, tags, blog_id, author_id))
                patched_blog = cursor.fetchone()
                print(patched_blog, "Patched Blog!")
                return {
                    "message": "Blog patched.",
                    "status": 200,
                    "blog_id": patched_blog[0],
                    "title": patched_blog[1],
                    "author_id": patched_blog[2],
                    "content": patched_blog[3],
                    "tags": patched_blog[4],
                    "date_published": patched_blog[5],
                    "image_url": patched_blog[7]
                }
            
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        print("Database error:", e)
        raise e