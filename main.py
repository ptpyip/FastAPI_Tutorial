from fastapi import FastAPI
from fastapi.params import Body

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
def createPost(payload: dict = Body(...)):  
    
    return payload
