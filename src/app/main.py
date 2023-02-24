from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

import schemas
import models
from app import database, crud

from config import FASTAPI_TUT_DATABASE_URL
   
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hi!"}

@app.post("/posts", 
          status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.Post, db: Session = Depends(connection)):  
    
    result = crud.createItem(
        table=models.Post,item=payload,session=db
    )
    
    if not result:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )
        
    return result

@app.get("/posts", response_model=List[schemas.PostResponse])
def read_all_posts(db: Session = Depends(connection)):
    results = crud.readAllItem(table=models.Post, session=db)
    
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
def read_posts(post_id: int, db: Session = Depends(connection)):
    # validateAndGetPost(post_id)
    results = crud.readItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not results:
        raise notFoundException(post_id)
    
    return {"data": results}

@app.put("/postLikes/{post_id}")
def update_postLikes(post_id: int, dislike: bool = False, db: Session = Depends(connection)):
    results = crud.updateItemById(**{
        "table": models.Post,
        "item_id": post_id,
        "set_values": {
            "likes": models.Post.likes + (1 - dislike*2)
        }
    }, session=db)

    if not results:
        raise notFoundException(post_id)

    return {"data": [results]}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int, db: Session = Depends(connection)):
    deleted_post = crud.deleteItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not deleted_post:
        raise notFoundException(post_id)
    
    return 

### Helper Functions

def notFoundException(id): 
    """ return Not Found Exception to client side"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{
            "loc": [
                "path",
                "post_id"
            ],
            "msg": f"Post with post_d={id} does not exists or ID our of range"
        }],           
    )

def main(db:Session = Depends(connection)):
    # posts = db.execute(
    #     select(models.Post)
    # )
    # # print(posts.mappings().all())
    # return posts.mappings().all()
    ...