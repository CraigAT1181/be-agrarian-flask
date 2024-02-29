from flask import jsonify

def fetch_all_produce(connection):
    try:
        query = """
        SELECT * FROM produce;
        """
    
        with connection.cursor() as cursor:
            cursor.execute(query)
            produce = cursor.fetchall()

            if produce:
                result = []
                
                for item in produce:
                    result.append({
                        "produce_id": item[0],
                        "produce_name": item[1],
                        "produce_type": item[2],
                        "produce_icon": item[3],
                        "produce_cat": item[4]
                    })
                return jsonify({"produce": result}), 200
            else:
                return jsonify({"message": "No produce found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching produce: {str(e)}"}), 500
