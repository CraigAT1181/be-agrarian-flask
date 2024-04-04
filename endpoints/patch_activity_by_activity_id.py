from flask import jsonify
from io import BytesIO
from PIL import Image
import psycopg2
import logging
from utils.cloud_authentication import cloud_authentication

def patch_activity_by_activity_id(user_id, title, activity_id, description, date_s_time, date_e_time, location, image, connection):
    
    def process_image(image, title):
        
        if image is None:
            return None
        
        if isinstance(image, str) and image.startswith('https://storage'):
            return image
    
        if hasattr(image, 'read'):
            filename = image.filename
            
            URLname = filename.split('.')[0]  # Get the title without the file extension

            content_type = "image/jpeg" if image.filename.lower().endswith(".jpeg") or image.filename.lower().endswith(".jpg") else "image/png"

            client = cloud_authentication()
            bucket_name = "cookingpot.live"
            
            blob_name = f"/images/activities/{URLname}.{content_type.split('/')[-1]}"
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
    
    
    updated_image_url = process_image(image, title)

    patch_activity = """
    UPDATE activities
    SET image_url = %s, title = %s, description = %s, date_s_time = %s, date_e_time = %s, location = %s, is_cancelled = %s
    WHERE activity_id = %s AND user_id = %s
    RETURNING *;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(patch_activity, (updated_image_url, title, description, date_s_time, date_e_time, location, False, activity_id, user_id))
                patched_activity = cursor.fetchone()
                
                return {
                    "message": "Activity updated.",
                    "status": 200,
                    "activity_id": patched_activity[0],
                    "user_id": patched_activity[1],
                    "title": patched_activity[2],
                    "description": patched_activity[3],
                    "date_s_time": patched_activity[4],
                    "date_e_time": patched_activity[5],
                    "location": patched_activity[6],
                    "image_url": patched_activity[7],
                    "is_cancelled": patched_activity[8],
                    "created_at": patched_activity[9],
                    "updated_at": patched_activity[10] 
                }
            
    except psycopg2.Error as e:
        # Log the database error for debugging
        logging.error(f"Database error: {e}")
        # Return an appropriate error response
        return jsonify({"message": "Failed to update the activity."}), 500