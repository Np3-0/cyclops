import firebase_admin
from firebase_admin import credentials

# Path to your downloaded private key file
cred = credentials.Certificate("service_key.json")

# Initialize the default app
def init():
    firebase_admin.initialize_app(cred)