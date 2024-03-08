from google.oauth2 import service_account
from google.cloud import storage
import os
import json

def cloud_authentication():
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    print(credentials_json, "CREDS")  # Print the JSON string
    if credentials_json:
        print("Reading render environment")
        try:
            # Parse the JSON string into a dictionary
            credentials_dict = json.loads(credentials_json)
            # If the environment variable is set, use its contents
            credentials = service_account.Credentials.from_service_account_info(credentials_dict)
            print(credentials, "credentials")
            client = storage.Client(credentials=credentials)
            print(client, "Got a client with render method")
            return client
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            raise  # Re-raise the exception to handle it elsewhere
    else:
        print("No render environment, so going for file")
        # If the environment variable is not set, check if the service account JSON file is available
        credentials_file_path = "db/data/agrarian-405810-5078dec12eaf.json"  # Update this with the actual file path
        if os.path.isfile(credentials_file_path):
            # If the JSON file is available, use it
            credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
            client = storage.Client(credentials=credentials)
            print("Got a client with file method")
            return client
        else:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set and service account JSON file is not found.")

