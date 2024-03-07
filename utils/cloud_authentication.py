from google.oauth2 import service_account
from google.cloud import storage
import os

def cloud_authentication():
    # Check if the environment variable is set
    credentials_dict = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_dict:
        # If the environment variable is set, use its contents
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        client = storage.Client(credentials=credentials)
        return client
    else:
        # If the environment variable is not set, check if the service account JSON file is available
        credentials_file_path = "db/data/agrarian-405810-5078dec12eaf.json"  # Update this with the actual file path
        if os.path.isfile(credentials_file_path):
            # If the JSON file is available, use it
            credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
            client = storage.Client(credentials=credentials)
            return client
        else:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set and service account JSON file is not found.")
