import firebase_admin
from firebase_admin import credentials, auth
import os

from django.conf import settings

# Initialize Firebase Admin SDK
SERVICE_ACCOUNT_KEY_PATH = os.path.join(settings.BASE_DIR, 'firebase-credentials.json') 

if not firebase_admin._apps:
    if os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
    else:
        # Fallback or strict error depending on deployment
        # print("Warning: Firebase Credentials not found. OTP verification will fail.")
        pass

def verify_firebase_token(id_token):
    try:
        # Allow 10 seconds of clock skew
        decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}") 
        return None
