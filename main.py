from fastapi import FastAPI

import Schema

posts_cache = []
    
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hellow Wrold"
    }
    
@app.get("/posts")
def viewPosts():
    return{
        "data": "This is a post"
    }    

@app.post("/posts")
def createPost(payload: Schema.Post):  
    
    return payload.dict()
