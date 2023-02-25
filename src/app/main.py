from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

import schemas
import models
from app import database, utils

from config import FASTAPI_TUT_DATABASE_URL

### Initialization
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hi!"}

### Operation on Posts

@app.post("/posts", 
          status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.Post, db: Session = Depends(connection)):  
    
    results = database.createItem(
        table=models.Post,item=payload.dict(),session=db
    )
    
    if not results:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )
        
    return results

@app.get("/posts", response_model=List[schemas.PostResponse])
def read_all_posts(db: Session = Depends(connection)):
    results = database.readAllItem(table=models.Post, session=db)
    
    if not results:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{
            "msg": f"No post exist",
            "data": results
        }],           
        )
    return {"data": results}
    
@app.get("/posts/{post_id}")
def read_post(post_id: int, db: Session = Depends(connection)):
    # validateAndGetPost(post_id)
    results = database.readItemById(
        table=models.Post, item_id=post_id, session=db
    )
    
    if not results:
        raise notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
    
    return {"data": results}

@app.put("/postLikes/{post_id}")
def update_postLikes(post_id: int, dislike: bool = False, db: Session = Depends(connection)):
    results = database.updateItemById(**{
        "table": models.Post,
        "item_id": post_id,
        "set_values": {
            "likes": models.Post.likes + (1 - dislike*2)
        }
    }, session=db)

    if not results:
        raise notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )

    return {"data": [results]}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int, db: Session = Depends(connection)):
    results = database.deleteItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not results:
        raise notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
    
    return 

### Operation on Users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(payload: schemas.UserIn, db: Session = Depends(connection)):
    hashed_pwd = utils.hashPassword(payload.input_pwd)
    
    results = database.createItem(
        table=models.User,
        item=payload.dict(exclude={"input_pwd"}) | {"hashed_pwd": hashed_pwd}, 
        session=db
    )
    
    if not results:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )

    return results
### Helper Functions

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(connection)):
    # validateAndGetPost(post_id)
    results = database.readItemById(
        table=models.User, item_id=user_id, session=db
    )
    
    if not results:
        raise notFoundException(
            msg=f"User with user_id={user_id} does not exists or ID our of range"
        )
    
    return {"data": results}

def notFoundException(msg): 
    """ return Not Found Exception to client side"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{
            "loc": [
                "path",
                "id"
            ],
            "msg": msg
        }],           
    )

def main(db:Session = Depends(connection)):
    # posts = db.execute(
    #     select(models.Post)
    # )
    # # print(posts.mappings().all())
    # return posts.mappings().all()
    ...