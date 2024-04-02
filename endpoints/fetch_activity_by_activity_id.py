from flask import jsonify
import logging

def fetch_activity_by_activity_id(connection, activity_id):
    if not activity_id:
        return jsonify({"message": "No activity_id received."}), 400

    query = """
    SELECT a.*, u.username
    FROM activities a
    JOIN users u ON u.user_id = a.user_id
    WHERE activity_id = %s;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (activity_id,))
                activity = cursor.fetchone()
                if activity:
                    return jsonify({
                        "activity_id": activity[0],
                        "user_id": activity[1],
                        "title": activity[2],
                        "description": activity[3],
                        "date_s_time": activity[4],
                        "date_e_time": activity[5],
                        "location": activity[6],
                        "image_url": activity[7],
                        "is_cancelled": activity[8],
                        "created_at": activity[9],
                        "updated_at": activity[10],
                        "username": activity[11]
                    })
                else:
                    return jsonify({"message": "Activity not found."}), 404
                
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An error occurred: " + str(e)}), 500
