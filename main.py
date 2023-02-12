from fastapi import FastAPI, HTTPException

import Schema

posts_cache = [
    {
        "id": 0,
        "title": "Testing post",
        "content": "This is a post for testing purposes",
        "published": True,
        "rating": 0
    }
]
    
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hellow Wrold"
    }
    
@app.get("/posts")
def readAllPosts():
    return {"data": posts_cache}

@app.get("/posts/{post_id}")
def readPosts(post_id: int):
    
    return {"data": posts_cache[post_id]}

@app.post("/posts")
def createPost(payload: Schema.Post):  
    new_id = len(posts_cache)
    new_post = {"id": new_id} | payload.dict()
    posts_cache.append(new_post)
    return {"data": new_post}
