from flask import jsonify, abort
import logging
import psycopg2

def patch_cancel_activity(activity_id, is_cancelled, connection):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE activities
                    SET is_cancelled = not %s
                    WHERE activity_id = %s
                    RETURNING *;
                    """,
                    (is_cancelled, activity_id)
                )
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
        logging.error(f"Database error occurred: {e}")
        abort(500, description="Database Error")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        abort(500, description="Internal Server Error")
