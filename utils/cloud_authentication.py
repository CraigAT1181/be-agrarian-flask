from google.oauth2 import service_account
from google.cloud import storage
import os
import json
import logging

def cloud_authentication():
    try:
        render_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')  
        if render_creds:          
            try:
                credentials_dict = json.loads(render_creds)
                credentials = service_account.Credentials.from_service_account_info(credentials_dict)
                client = storage.Client(credentials=credentials)
                return client
            except json.JSONDecodeError as e:
                logging.error("Error decoding JSON credentials: %s", e)
                raise
        else:
            credentials_file_path = "db/data/agrarian-405810-5078dec12eaf.json"
            if os.path.isfile(credentials_file_path):
                credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
                client = storage.Client(credentials=credentials)
                return client
            else:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set and service account JSON file is not found.")        
    except Exception as e:
        logging.error("Error during cloud authentication: %s", e)
        raise

