from django.http import JsonResponse
from firebase_admin import auth
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError

# firebase user auth decorator
def firebase_auth_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"message": "Unauthorized"}, status=401)
        
        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.firebase_user = decoded_token
        except ExpiredIdTokenError:
            return JsonResponse({"message": "Token expired"}, status=401)
        except InvalidIdTokenError:
            return JsonResponse({"message": "Invalid token"}, status=401)
        except Exception as e:
            return JsonResponse({"message": f"Authentication error: {str(e)}"}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view