import firebase_admin
from firebase_admin import credentials
from django.conf import settings

def initialize_firebase_admin():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS)
        firebase_admin.initialize_app(cred)

# Initialize Firebase Admin when this module is imported
initialize_firebase_admin()

