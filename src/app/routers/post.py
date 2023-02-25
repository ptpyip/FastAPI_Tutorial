from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
import views
from app import database, utils

from config import FASTAPI_TUT_DATABASE_URL

### Initialization
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

### Operation on Posts

@router.post("/", 
          status_code=status.HTTP_201_CREATED, response_model=views.PostDisplay)
def create_post(payload: schemas.Post, db: Session = Depends(connection)):  
    
    results = database.createItem(
        table=models.Post,item=payload.dict(),session=db
    )
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )
        
    return results

@router.get("/", response_model=List[views.PostDisplay])
def read_all_posts(db: Session = Depends(connection)):
    results = database.readAllItem(table=models.Post, session=db)
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{
                "msg": f"No post exist",
                "data": results
            }],           
        )
    return results
    
@router.get("/{post_id}", response_model=views.PostDisplay)
def read_post(post_id: int, db: Session = Depends(connection)):
    # validateAndGetPost(post_id)
    results = database.readItemById(
        table=models.Post, item_id=post_id, session=db
    )
    
    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
        
    return results

@router.put("/likes/{post_id}", response_model=views.PostDisplay)
def update_postLikes(post_id: int, dislike: bool = False, db: Session = Depends(connection)):
    results = database.updateItemById(**{
        "table": models.Post,
        "item_id": post_id,
        "set_values": {
            "likes": models.Post.likes + (1 - dislike*2)
        }
    }, session=db)

    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )

    return results

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int, db: Session = Depends(connection)):
    results = database.deleteItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
    
    return 

