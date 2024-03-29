from flask import jsonify
import logging
import psycopg2

def fetch_activities_by_user_id(connection, user_id):

    try:
        if not user_id:
            return jsonify({"message": "No user_id received."}), 400

        query = """
            SELECT a.*, u.username
            FROM activities a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.user_id = %s
            ORDER BY a.updated_at DESC;
        """
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
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
                        "created_at": activity[8],
                        "updated_at": activity[9]
                    })
                    
                return jsonify({"activities": result}), 200
        
    except psycopg2.Error as e:
        logging.error(f"Database error occurred: {e}")
        return jsonify({"message": "Database error occurred."}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500