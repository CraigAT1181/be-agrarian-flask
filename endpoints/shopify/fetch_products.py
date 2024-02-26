from flask import jsonify
import requests
import os

def fetch_products(data):
    try:
        query = data.get("query")
        print(query, "GET PRODUCTS")
        response = requests.post(
            "https://cookingpotcic.myshopify.com/admin/api/2022-04/graphql.json",
            json={"query": query},
                        headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN"),
            },
        )

        # Return the response from the Shopify API to the frontend
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500