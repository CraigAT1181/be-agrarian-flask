from flask import jsonify

def fetch_all_produce(connection):
    query = """
    SELECT * FROM produce;
    """

    with connection:
        cursor = connection.cursor()
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
            return None
            