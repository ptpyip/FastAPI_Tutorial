from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models
from app import database

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
def create_post(payload: schemas.Post):  
    
    new_post = postDB.execute("""
        INSERT INTO "Posts" (title, is_published, content)
        VALUES (%s, %s, %s)
        RETURNING *;
    """, (payload.title, payload.is_published, payload.content)
    )
    
    return {"data": new_post[0]}

@app.get("/posts")
def read_all_posts(db: Session = Depends(connection)):
    
    # posts = postDB.execute("""
    #     SELECT * FROM "Posts"
    # """)
    # return {"data": posts}
    
    results = db.execute(
        select(models.Post)
    ).mappings()
    return {"data": [result['Post'] for result in results.all()]}
    

@app.get("/posts/{post_id}")
def read_posts(post_id: int):
    # validateAndGetPost(post_id)
    post_fetched = postDB.execute("""
        SELECT * FROM "Posts" WHERE post_id = %s
    """, (f"{post_id}",), fetching_all=False)
    
    if not post_fetched:
        raise notFoundException(post_id)
    
    return {"data": post_fetched}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int):
    deleted_post = postDB.execute("""
        DELETE FROM "Posts" WHERE post_id = %s
        RETURNING *;
    """, (f"{post_id}",), fetching_all=False)
    
    if not deleted_post:
        raise notFoundException(post_id)
    
    return 

@app.put("/postLikes/{post_id}")
def update_postLikes(post_id: int, dislike: bool = False):
    post_updated = postDB.execute("""
        UPDATE "Posts" SET likes = likes + %s WHERE post_id = %s
        RETURNING *;
    """, (f"{1 - dislike*2}",f"{post_id}"), fetching_all=False)
    
    if not post_updated:
        raise notFoundException(post_id)
    
    return {"data": post_updated}


def main(db:Session = Depends(connection)):
    posts = db.execute(
        select(models.Post)
    )
    # print(posts.mappings().all())
    return posts.mappings().all()
