from flask import jsonify
import logging

def fetch_all_produce(connection):

    query = """
    SELECT * FROM produce;
    """

    try:
        with connection:    
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
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": f"Error fetching produce: {str(e)}"}), 500
