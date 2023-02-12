from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
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

@app.post("/post")
def createPost(payload:Post):  
    
    return payload.dict()
