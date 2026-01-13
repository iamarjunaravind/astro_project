import firebase_admin
from firebase_admin import credentials, auth
import os

from django.conf import settings

# Initialize Firebase Admin SDK
import json

SERVICE_ACCOUNT_KEY_PATH = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')

if not firebase_admin._apps:
    try:
        # Check for environment variable first (Production/Hosting)
        firebase_creds_json = os.environ.get('FIREBASE_CREDENTIALS')
        
        if firebase_creds_json:
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized with environment variables.")
        elif os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            # Fallback to file (Local Development)
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized with local file.")
        else:
            print("Warning: Firebase Credentials not found (Env 'FIREBASE_CREDENTIALS' or file). OTP verification may fail.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        pass

def verify_firebase_token(id_token):
    try:
        # Allow 10 seconds of clock skew
        decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}") 
        return None
