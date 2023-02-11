# Python FastAPI Full Course

Last Update: 11/02/23

## A. Course Contents

### Part I: FastAPI Basic
#### 1. Setup Virtual Enlivenment
``` zsh
$ python -m venv venv       
$ source venv/bin/activate
$ pip install "fastapi[all]"   
```
- Create the virtual environment folder `/venv`
- After activate the venv, install all dependencies of FastAPI  

#### 2. The First Steps
``` zsh
$ uvicorn <fileName>:<FastAPIObjName> --reload
```
- Start the Uvicorn server

#### 3. Postman + POST method in FastAPI
``` python
@app.post("/item")
def createPost(payload: dict = Body(...)):  
    # Extract all the field from Body and covert to dict
    return payload
```

### Part II: Database Basic

### Part III: Backend Basic

### Part IV: Deployment -- Microservices

### Part V: Testing 

### Part VI: DevOp -- CI/CD