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

  #### 7. Dependency Injection

2. Raise an exception with custom exception handlers

### Part II: Database in Python
#### 1. Connect to Postgres DB 
- Use psycopg3 lib
- How to use:
  ``` python
    import psycopg      # psycopg3
    from psycopg.rows import dict_row       # dict_row allows return data as dict

    def retriveData(connect_info, query, params=None, fetching_all=True) -> list:
        with psycopg.connect(connect_info, row_factory=dict_row) as conn:   
            with conn.cursor() as cur:
                cur.execute(query, params)

                if fetching_all:
                    results = cur.fetchall() 
                else:
                    results = cur.fetchone()

                conn.commit()  
        
        return results
  ``` 

#### 2. CRUD with DataBase
- Create:
  - Insert row + getting back inserted data 
  - If return None -> error occurred.
  ``` python
    execute("""
        INSERT INTO "Items" (name, content)
        VALUES (%s, %s)
        RETURNING *;    
    """, (payload.name, payload.is_publicontentshed))
  ```

- Read -> GET
  ``` python
    execute("""
        SELECT * FROM "Items" WHERE id = %s
    """, (f"{id}",))
  ``` 

- Update -> PUT
  ``` python
    execute("""
        UPDATE "Items" SET quantity = quantity + %s WHERE id = %s
        RETURNING *;
    """, (f"{-1}",f"{id}"))
  ``` 

- Delete -> DELETE
  ``` python
    execute("""
        DELETE FROM "Items" WHERE id = %s
        RETURNING *;
    """, (f"{id}",))
  ``` 

#### 3. Intro to ORM
- ORM: Object Relation Mapping
  -> ABS layer between code and db
  -> Translate code to SQL and communicate with db.
- Benefits:
  - No SQL!
  - Fully use Python 
    -> define table as Python models 
    -> more readable query

#### 4. Declare Models
``` python
    from typing import List, Optional
    from sqlalchemy import String, ForeignKey
    from sqlalchemy.orm import Mapped, mapped_column
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        pass

    class Item(Base):
        __tablename__ = "Items" 

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str]
        default_val_field: Mapped[bool] = mapped_column(default=True)\
        optional_field: Mapped[Optional[str]]
        
        def __repr__(self) -> str:
            return f"Item(id={self.id!r}, name={self.name!r})"

```
#### 5. Set up SQLAlchemy
```python
    import models 

    def getPostgresURL(dbms, postgresserver, dbname, user, pwd):
        return f"{dbms}://{user}:{pwd}@{postgresserver}/{dbname}"

    def main():
        engine = create_engine(
            url=FASTAPI_TUT_DATABASE_URL, echo=True
        )
        models.Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(engine, autoflush=False,autobegin=False)
```

### 6. Query on SQLAlchemy 
``` python
    db = SessionLocal()
    db.begin()

    results = db.execute(
            select(models.Item)
        ).mappings()
        return {"data": [result['Item'] for result in results.all()]}
```

### 7. SQLAlchemy in Fast API 
- require Dependency Injection
- function as dependencies:
  ``` python
      def get_db():
          db = SessionLocal()
          try:
              yield db
          finally:
              db.close()

      def read_items(db: Session = Depends(get_db)):
        ...
  ```
- class as dependencies:
  ``` python
      class Connection():
    
          def __init__(self) -> None:
              engine = create_engine(
                  url=FASTAPI_TUT_DATABASE_URL, echo=True
              )
              
              models.Base.metadata.create_all(engine)
              
              self.SessionLocal = sessionmaker(engine, autoflush=False,autobegin=False)
          
          def __call__(self):
              db = self.SessionLocal()
              db.begin()
              try:
                  yield db
              finally:
                  db.close()

      connection = Connection()
      def read_items(db: Session = Depends(connection)):
        ...
  ```


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