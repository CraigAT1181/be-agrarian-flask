from flask import jsonify
from io import BytesIO
from PIL import Image
import psycopg2
from utils.cloud_authentication import cloud_authentication

def patch_blog_by_blog_id(blog_id, image, title, author_id, content, tags, connection):
    try:

        if not blog_id:
            return jsonify({"message": "No blog_id received."}), 400
        
        if image.startswith('https://storage'):
            with connection:
                with connection.cursor() as cursor:
                    
                    cursor.execute("""
                        UPDATE blogs
                        SET title = %s, content = %s, tags = %s
                        WHERE blog_id = %s AND author_id = %s
                        RETURNING *;
                    """, (title, content, tags, blog_id, author_id))
                    
                    updated_blog = cursor.fetchone()

                    if updated_blog is not None:
                        return jsonify({"message": "Blog updated successfully.", "blog": updated_blog}), 200
                    else:
                        return jsonify({"message": "Blog not found."}), 404
        
        if image is None:
            image_url = None
        
        else:
            content_type = "image/jpeg" if image.filename.lower().endswith(".jpeg") or image.filename.lower().endswith(".jpg") else "image/png"
            print("REACHED HERE")
            client = cloud_authentication()
            print(client, "authed!")
            bucket_name = "cookingpot.live"
            blob_name = f"/images/blogs/{title}.{content_type.split('/')[-1]}"
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            print("AUTHENTICATED")
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
    
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute("""
                    UPDATE blogs
                    SET image_url = %s, title = %s, content = %s, tags = %s
                    WHERE blog_id = %s AND author_id = %s
                    RETURNING *;
                """, (image_url, title, content, tags, blog_id, author_id))
                
                updated_blog = cursor.fetchone()

                if updated_blog is not None:
                    return jsonify({"message": "Blog updated successfully.", "blog": updated_blog}), 200
                else:
                    return jsonify({"message": "Blog not found."}), 404

    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        print("Database error:", e)
        return jsonify({"message": "Unable to process this request due to a database error"}), 500
