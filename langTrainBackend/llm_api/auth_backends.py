from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from firebase_admin import auth
from .firebase_utils import sync_firebase_user_to_django

User = get_user_model()

class FirebaseBackend(ModelBackend):
    def authenticate(self, request, firebase_token=None, **kwargs):
        if firebase_token:
            try:
                decoded_token = auth.verify_id_token(firebase_token)
                uid = decoded_token['uid']
                firebase_user = auth.get_user(uid)
                return sync_firebase_user_to_django(firebase_user)
            except:
                return None
        return None