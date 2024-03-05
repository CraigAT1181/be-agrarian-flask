from google.oauth2 import service_account
from google.cloud import storage

def authenticate_with_gcp(credentials_file_path):
    """Authenticate with Google Cloud Platform using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = storage.Client(credentials=credentials)
    return client