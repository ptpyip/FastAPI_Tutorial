from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app import database, utils
from .routers import post, user

from config import FASTAPI_TUT_DATABASE_URL

### Initialization
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hi!"}

def main():
    # posts = db.execute(
    #     select(models.Post)
    # )
    # # print(posts.mappings().all())
    # return posts.mappings().all()
    ...