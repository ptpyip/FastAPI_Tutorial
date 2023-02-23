from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

import schemas
import models
from app import database, crud

CONNECTION_INFO = "host=localhost dbname=fastapiTut user=postgres password=1234"

posts_cache = [
    {
        "id": 0,
        "title": "Testing post",
        "content": "This is a post for testing purposes",
        "published": True,
        "likes": 0
    }
]

def validateAndGetPost(post_id: int):
    # print(post_id)
    if (post_id < len(posts_cache)) or post_id >= 0: 
        return posts_cache[post_id]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{
            "loc": [
                "path",
                "post_id"
            ],
            "msg": f"Post {post_id} does not exists or ID our of range"
        }],           
    )
    
def notFoundException(id): 
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
   
postDB = database.setConnection()
connection =  database.Connection()

# db = database.connect()
# db.begin()
 
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hi!"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
        
    return {"data":[result]}

@app.get("/posts")
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

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int, db: Session = Depends(connection)):
    deleted_post = crud.deleteItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not deleted_post:
        raise notFoundException(post_id)
    
    return 

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


def main(db:Session = Depends(connection)):
    # posts = db.execute(
    #     select(models.Post)
    # )
    # # print(posts.mappings().all())
    # return posts.mappings().all()
    ...