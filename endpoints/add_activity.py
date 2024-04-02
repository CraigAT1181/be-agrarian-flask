from io import BytesIO
from PIL import Image
from psycopg2 import IntegrityError
from utils.cloud_authentication import cloud_authentication
import logging

def add_activity(user_id, title, description, date_s_time, date_e_time, location, image, connection):
    try:
        # Check if title and content are provided
        if not all([title, description, date_s_time, date_e_time, location]):
            raise ValueError("Activity must contain a title, description, date/time and location.")

        # Set image to None if not provided
        if image is None:
            image_url = None
        else:
            # Determine content type based on file extension
            content_type = "image/jpeg" if image.filename.lower().endswith(".jpeg") or image.filename.lower().endswith(".jpg") else "image/png"
            
            # Authenticate cloud client
            client = cloud_authentication()
            bucket_name = "cookingpot.live"
            blob_name = f"/images/activities/{title}.{content_type.split('/')[-1]}"
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
        insert_activity = """
        INSERT INTO activities
        (user_id, title, description, date_s_time, date_e_time, location, image_url, is_cancelled)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(insert_activity, (user_id, title, description, date_s_time, date_e_time, location, image_url, False))
                new_activity = cursor.fetchone()
                
                return {
                    "message": "Activity created.",
                    "status": 200,
                    "activity_id": new_activity[0],
                    "user_id": new_activity[1],
                    "title": new_activity[2],
                    "description": new_activity[3],
                    "date_s_time": new_activity[4],
                    "date_e_time": new_activity[5],
                    "location": new_activity[6],
                    "image_url": new_activity[7],
                    "is_cancelled": new_activity[8],
                    "created_at": new_activity[9],
                    "updated_at": new_activity[10]   
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
                "message": "Activity already exists.",
                "status": 409,
            }
        else:
            logging.error(f"Error inserting activity into database: {e}")
            return {
                "message": "An error occurred while creating the activity.",
                "status": 500,
            }
    except Exception as e:
        # Handle unexpected exceptions
        logging.error(f"An unexpected error occurred: {e}")
        return {
            "message": "An unexpected error occurred.",
            "status": 500,
        }
