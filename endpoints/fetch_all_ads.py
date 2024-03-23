from flask import jsonify
import logging

def fetch_all_ads(connection):
    
    query = """
    SELECT * FROM ads;
    """

    try:
        with connection:
            with connection.cursor() as cursor:
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
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "Error fetching ads."}), 500