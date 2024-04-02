from flask import jsonify
import logging

def fetch_all_activities(connection):

    query = """
    SELECT a.*, u.username  
    FROM activities a
    JOIN users u ON u.user_id = a.user_id
    ORDER BY a.updated_at DESC;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                activities = cursor.fetchall()
                result = []
                
                for activity in activities:
                    result.append({
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

                return jsonify({"activities": result}), 200
            
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": f"Error fetching activities: {str(e)}"}), 500
