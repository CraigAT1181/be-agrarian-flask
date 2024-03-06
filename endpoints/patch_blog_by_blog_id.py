from flask import jsonify
import psycopg2
from utils.cloud_authentication import cloud_authentication

def patch_blog_by_blog_id(data, blog_id, connection):
    if not blog_id:
        return jsonify({"message": "No blog_id received."}), 400

    author_id = data.get("author_id")
    if not author_id:
        return jsonify({"message": "No author_id received."}), 400

    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")
    image_data = data.get("image_data")

    try:
        with connection:
            with connection.cursor() as cursor:
                # Check if image data is provided for update
                if image_data:
                    # Authenticate with Google Cloud Storage and upload the new image
                    client = cloud_authentication("db/data/agrarian-405810-5078dec12eaf.json")
                    
                    bucket_name = "cookingpot.live"
                    blob_name = f"images/{title}.jpg"
                    bucket = client.get_bucket(bucket_name)
                    blob = bucket.blob(blob_name)

                    content_type = "image/jpeg" if image_data.startswith(b"\xFF\xD8") else "application/octet-stream"

                    blob.upload_from_string(image_data, content_type=content_type)

                    new_image_url = blob.public_url

                    cursor.execute("""
                        UPDATE blogs
                        SET image_url = %s
                        WHERE blog_id = %s AND author_id = %s
                        RETURNING *
                    """, (new_image_url, blog_id, author_id))
                    updated_blog = cursor.fetchone()

                    if updated_blog is not None:
                        return jsonify({"message": "Blog updated successfully.", "blog": updated_blog}), 200
                    else:
                        return jsonify({"message": "Blog not found."}), 404
                else:
                    # Update other fields if no image data provided
                    cursor.execute("""
                        UPDATE blogs
                        SET title = %s, content = %s, tags = %s
                        WHERE blog_id = %s AND author_id = %s
                        RETURNING *
                    """, (title, content, tags, blog_id, author_id))
                    updated_blog = cursor.fetchone()

                    if updated_blog is not None:
                        return jsonify({"message": "Blog updated successfully.", "blog": updated_blog}), 200
                    else:
                        return jsonify({"message": "Blog not found."}), 404

    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        print("Database error:", e)
        return jsonify({"message": "Unable to process this request due to a database error"}), 500
