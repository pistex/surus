from google.cloud import secretmanager
from .initialization import gcp_initailize

gcp_initailize()
secret_client = secretmanager.SecretManagerServiceClient()

def get_secret_version(secret_name):
    secret = secret_client.access_secret_version(name=secret_name)
    return secret.payload.data.decode('utf-8')
