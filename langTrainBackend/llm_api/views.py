from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from .languageModel import get_response_openai, get_response_qwen, get_response_llama3,get_response_ollama
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .decorators import firebase_auth_required
from rest_framework.response import Response
# ----------------- Firebase database packages ------------- #
from firebase_admin import firestore, auth
from django.contrib.auth.hashers import make_password
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError

# example of of django page rendering
from django.shortcuts import render
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')


# large language model function call

# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# This decorator verify users identity from firebase

# how to get access token from firebase?
# post link to following URL to firebase with body
# https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<Web API Key>

# how to get web API key?
# login to firebase 
# -> click project 
# -> click setting icon next to project overview on left top side 
# -> click project setting
# -> web API is in general setting

# post body should be like this
'''
{
  "email": "test@gmail.com",
  "password": "test123",
  "returnSecureToken": true
}
'''
# example of javascript fetching
'''
fetch('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<your_web_api_key>', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'test@gmail.com',
    password: 'test123',
    returnSecureToken: true
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
'''

# example fetch request
'''
    const response = await fetch('http://127.0.0.1:8000/api/llama31/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: input })
    });

'''


# openai 
# creaate .env under app folder  
# └───llm_api
#     └───.env
# with:
# OPENAI_API_KEY=yourkey

@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@firebase_auth_required
def openai(request):
    try:
        user_input = request.data.get('input')
        if not user_input:
            return JsonResponse({'error': 'No input provided'}, status=status.HTTP_400_BAD_REQUEST)

        data = get_response_openai(user_input)
        return JsonResponse(data, safe=False, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Qwen2

@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def qwen(request):
    try:
        user_input = request.data.get('input')
        if not user_input:
            return JsonResponse({'error': 'No input provided'}, status=status.HTTP_400_BAD_REQUEST)

        data = get_response_qwen(user_input)
        return JsonResponse(data, safe=False, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Llama3.1
@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@firebase_auth_required
def llama3(request):
    try:
        user_input = request.data.get('input')
        if not user_input:
            return JsonResponse({'error': 'No input provided'}, status=status.HTTP_400_BAD_REQUEST)

        data = get_response_llama3(user_input)
        return JsonResponse(data, safe=False, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# groq Api, combinate Groq with openai api for instance speech ouput
# Llama3.1 + ChatTTS for free user
@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@firebase_auth_required
def groq(request):
    pass
    return None

# Example of post request to database
# add this line if user auth is required
# @firebase_auth_required
@api_view(['POST'])
def post_db(request):
    if request.method == 'POST':
        # get Json body value
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not all([username, password]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Hash the password or API
            hashed_password = make_password(password)
            
            # Add data to Firestore
            db = firestore.client()
            # UserInfo is document/table name, by post request, use 'add' method add user data into database
            doc_ref = db.collection('UserInfo').add({
                'username': username,
                'password': hashed_password  # Store hashed password
            })
            
            # Get the autogenerated document ID, simulate primary key in relational database
            doc_id = doc_ref[1].id
            
            return Response({"message": "User added successfully", "doc_id": doc_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
# step 1 handle Post request like step 
# https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<webID>
# example output
'''
{ "kind": "identitytoolkit#VerifyPasswordResponse", 
"localId": "sUwbRt1XUtTg2PfP2N5uC223pjL2", 
"email": "test@gmail.com", "displayName": "", 
"idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbGFuZ3RlYWNoLThkNjRhIiwiYXVkIjoibGFuZ3RlYWNoLThkNjRhIiwiYXV0aF90aW1lIjoxNzIyMzcyNTI3LCJ1c2VyX2lkIjoic1V3YlJ0MVhVdFRnMlBmUDJONXVDMjIzcGpMMiIsInN1YiI6InNVd2JSdDFYVXRUZzJQZlAyTjV1QzIyM3BqTDIiLCJpYXQiOjE3MjIzNzI1MjcsImV4cCI6MTcyMjM3NjEyNywiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.Jkd7Cui2OmcPEVQJRTE99WE8JFxQz7G33IMHM0XPAKm9Dg84mNjtoOHYt1tlg8Zph8GJPM-Ivi-2QgSgRGBNSx0xeds_3Hhmv0HZ7Z7WW6k0Dvaq5oViGgza5vc5J1lx25MDVziqy5SSu7A7ifAbXtoC8ScF6HHGNWmrOkXHYeWG9GdR1H8nuUQM58qDhyChp5hlTo9e6daGfeN7BrXYjKRUEhpEWBmBhjOx5HlFViK1hri6cbDu7gS8x8KQUkDNBx9F_Hp42P1jsAk1X0OaQgO5lzLbr3fPD-QugE30D4y8RcLWBBNDYcEuPSJSfh9BoPoNPp0WcpyJIoLtOgWDoQ", 
"registered": true, "refreshToken": "AMf-vBxZQXmMuRQUM1EuFXr3kFNoXHVqERZwi9TW83pflZLX1GEiB5A_1ajLnHD0vq-BK2mmoVY1hsoAT75J93-t5mYEEXtko7BbDc9DFJnP5ArcQ-n5HQApdpiOkhbRXZTAxXgqmE1tlMCXk6b5fJXugprRED4zg_aQ_uEkLvXcqlHFNxNy1mZrSOYZVpFnYu-0QUifB30s88DtnnM-rYnzAx-PRMlR4A", 
"expiresIn": "3600" }
'''
# step 2 request backend service with Token
'''
headers: {
            Authorization: `Bearer ${idToken}`
          }
'''
# test this endpoint with postman
@api_view(['GET'])
@firebase_auth_required
def secret(request):
    return JsonResponse({
        "message": "Success",
        "user": request.firebase_user.get('email')  # Adjust this based on your user attribute
    })
