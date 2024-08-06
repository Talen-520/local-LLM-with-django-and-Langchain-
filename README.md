# Connect local LLM with Django

## Clone this repository, do as following

### 1. create virtual environment
```
python -m venv venv
```
### 2. activate virtual environment
```
.\venv\Scripts\activate
```

### 3. install packages into virtual environment

```
pip install -r requirements.txt
```
### start your server
```
cd .\langTrainBackend\
python manage.py runserver
```


### install ollama

[Download](https://ollama.com/download/)
### run ollama
```
ollama serve
```
You need to keep this service running whenever you are using [ollama](https://github.com/ollama/ollama)  


### pull model checkpoint
> [!NOTE]
> You only need pull one model for each URL endpoint, for example, in order to access http://127.0.0.1:8000/api/llama31/
> run  ollama pull llama3.1

```
# 7b model, system prompt not supported, 4.4 GB
ollama run qwen2:7b

# 72b model support system prompt, size 41 GB this is optional
ollama run qwen2:72b

# llama3.1 most advanced open source model, for langchain implementation see documentation 
# https://python.langchain.com/v0.1/docs/integrations/chat/ollama/
ollama pull llama3.1

```

### Example of Input and Ouput 

get access
```
URL
https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<firebase Web ID>
Body
{
  "email": "test@gmail.com",
  "password": "test123",
  "returnSecureToken": true
}
output
{
    "kind": "identitytoolkit#VerifyPasswordResponse",
    "localId": <userID>,
    "email": <email>,
    "displayName": <name>,
    "idToken": <idToken>,
    "registered": true,
    "refreshToken": <user refresh Token>,
    "expiresIn": "3600"
}

```
### pass idToken to requested URL
```
URL
http://127.0.0.1:8000/api/llama3/
{
    
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }

    "input": "Hello"
    }

output
{"response": string, 
 "time": string, 
 "tokens": int}
```

## Javascript 
### post request to Firebase auth 
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

### Example fetch request for LLM response
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

