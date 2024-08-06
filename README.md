# LangTrain
LangTrain your Mandarin AI teacher


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
### run backend service
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

```
# 7b model, system prompt not supported, 4.4 GB
ollama run qwen2:7b

# support system prompt,size 41 GB this is optional
ollama run qwen2:72b

# llama3 might not good for chinese language, see documentation 
# https://python.langchain.com/v0.1/docs/integrations/chat/ollama/
ollama pull llama3.1

```

### test endpoint with RAW JSON INPUT - you need openai Key for this endpoint
```
http://127.0.0.1:8000/api/openai/
{
    
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }

    "input": "Hello"
    }
    
```

### test endpoint with RAW JSON INPUT - you need install ollama and Qwen2
```
http://127.0.0.1:8000/api/qwen/
{"input": "Hello"}
```

### test endpoint with RAW JSON INPUT - you need install ollama and llama3 as step above
```
http://127.0.0.1:8000/api/llama3/
{
    
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }

    "input": "Hello"
    }
```

output format:
```
{"response": string, 
 "time": string, 
 "tokens": int}
```