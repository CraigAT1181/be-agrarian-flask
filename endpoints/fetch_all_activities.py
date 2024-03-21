from flask import jsonify

def fetch_all_activities(connection):
    try:
        query = """
        SELECT a.*, u.username  
        FROM activities a
        JOIN users u ON u.user_id = a.user_id
        ORDER BY a.updated_at DESC;
        """

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
                    "datetime": activity[4],
                    "location": activity[5],
                    "image_url": activity[6],
                    "created_at": activity[7],
                    "updated_at": activity[8],
                    "username": activity[9]
                })

            return jsonify({"activities": result}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching blogs: {str(e)}"}), 500
