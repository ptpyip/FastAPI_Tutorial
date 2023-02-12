from fastapi import FastAPI, HTTPException, status

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
    if post_id >= len(posts_cache):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{
                "loc": [
                    "path",
                    "post_id"
                ],
                "msg": "Post does not exists or ID our of range"
            }],           
        )
    return {"data": posts_cache[post_id]}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(payload: Schema.Post):  
    new_id = len(posts_cache)
    new_post = {"id": new_id} | payload.dict()
    posts_cache.append(new_post)
    return {"data": new_post}
