from google.oauth2 import service_account
from google.cloud import storage

def cloud_authentication(credentials_file_path):
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = storage.Client(credentials=credentials)
    return client