from flask import jsonify
import requests
import os
import logging

def fetch_products(data):
    try:
        query = data.get("query")
        response = requests.post(
            "https://cookingpotcic.myshopify.com/admin/api/2024-01/graphql.json",
            json={"query": query},
                        headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN"),
            },
        )

        logging.info(f"Request to Shopify API successful. Status code: {response.status_code}")
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        logging.error(f"Error fetching products from Shopify API: {e}")
        return jsonify({"error": str(e)}), 500