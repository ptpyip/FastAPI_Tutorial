# Python FastAPI Full Course

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
$ uvicorn <folder.fileName>:<FastAPIObjName> --reload
```
- Start the Uvicorn server

#### 3. Postman + POST method in FastAPI
``` python
@app.post("/item")
def createPost(payload: dict = Body(...)):  
    # Extract all the field from Body and covert to dict
    return payload.dict()
```

#### 4. Schema, using Pydantic
``` python
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):      # create a pydantic model for FastAPI Schema
    title: str
    content: str
    default_val_field: bool = True
    optional_field: Optional[int] = None

```
- Allow validation -> use Pydantic

- [Note](#1-schema)

#### 5. CRUD Operation & RESTful API
- Create -> POST
  ``` python
  from fastapi import status
  @app.post("/item", status_code=status.HTTP_201_CREATED)
  ```

- Read -> GET
  ``` python
  @app.get("/items/{id}")
  def readItems(id: int):
      return {"data": item[id]}

  ``` 
- Update -> PUT
- Delete -> DELETE

#### 6. Error Handling
1. Raise an `HTTPException` 
   ``` python
   from fastapi import HTTPException
   @app.get("/items/{id}")
   def readItems(id: int):
        if id >= len(posts_cache):
            raise HTTPException(
                status_code=404,
                detail={
                    "loc": ["path","id"],
                    "msg": "item does not exists or ID our of range"
                },           
                header{},
            )
   ``` 

2. Raise an exception with custom exception handlers

### Part II: Database Basic

### Part III: Backend Basic

### Part IV: Deployment -- Microservices

### Part V: Testing 

### Part VI: DevOp -- CI/CD


## B. Peronal Notes
### 1. Schema
Use a seperate `/Schema` dir to store schemas
```
Schema/
  __init__.py
  Model1.py
```


Last Update: 12/02/23