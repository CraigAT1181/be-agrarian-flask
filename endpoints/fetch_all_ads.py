from flask import jsonify

def fetch_all_ads(connection):
    
    query = """
    SELECT * FROM ads;
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query)
        ads = cursor.fetchall()
        result = []
        
        for ad in ads:
            result.append({
                "ad_id": ad[0],
                "image_url": ad[1],
                "redirect_url": ad[2]
            })

        return jsonify({"ads": result}), 200