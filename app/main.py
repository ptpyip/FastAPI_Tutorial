from fastapi import FastAPI, HTTPException, status

import Schema
from app.PostDB import PostDB

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
    

postDB = PostDB(connect_info=CONNECTION_INFO)
 
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hellow Wrold"
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Schema.Post):  
    new_id = len(posts_cache)
    new_post = {"id": new_id} | payload.dict()
    posts_cache.append(new_post)
    
    
    return {"data": new_post}

@app.get("/posts")
def read_all_posts():
    posts = postDB.execute("""
        SELECT * FROM "Posts"
    """)
    return {"data": posts}

@app.get("/posts/{post_id}")
def read_posts(post_id: int):
    validateAndGetPost(post_id)
    
    return {"data": posts_cache[post_id]}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int):
    validateAndGetPost(post_id)
    
    deleted_post = posts_cache.pop(post_id)
    return 

@app.put("/postLikes/{post_id}")
def update_postLikes(post_id: int, like: bool = True):
    post = validateAndGetPost(post_id)
    # posts_cache[post_id] += like*1 -(not like)*1
    
    post["likes"] += 1 if (like) else -1
    
    if post["likes"] < 0: 
        post["likes"] = 0
    return {"data": post}
