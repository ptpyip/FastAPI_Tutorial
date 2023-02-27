from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
from app import database, utils, security

from config import FASTAPI_TUT_DATABASE_URL

### Initialization
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

authorized_users = security.AuthorizedUser()

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

### Operation on Posts

@router.post("/", 
          status_code=status.HTTP_201_CREATED, response_model=schemas.PostDisplayView)
def create_post(payload: schemas.Post, current_user: schemas.TokenData = Depends(authorized_users), db: Session = Depends(connection)):  
    new_post = payload.dict() | {"owner_id": current_user.user_id}
    results = database.createItem(
        table=models.Post,item=new_post ,session=db
    )
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )
    
    # print(current_user)
        
    return results

@router.get("/", response_model=List[schemas.PostDisplayView])
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
    
@router.get("/{post_id}", response_model=schemas.PostDisplayView)
def read_post(post_id: int, db: Session = Depends(connection)):
    return __get_post(post_id, db)

@router.get("/{user_id}", response_model=List[schemas.PostDisplayView])
def read_post_by_user(user_id: int, db: Session = Depends(connection)):
    results = database.readItems(
        table=models.Post,
        filters=[models.Post.owner_id == user_id],
        fetching_all=True,
        session=db
    )
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{
                "msg": f"No post exist",
                "data": results
            }],           
        )
        
    return results

@router.put("/likes/{post_id}", response_model=schemas.PostDisplayView)
def update_postLikes(
    post_id: int, dislike: bool = False, 
    current_user: schemas.TokenData = Depends(authorized_users), db: Session = Depends(connection)
):
    post = __get_post(post_id, db)
    
    if post.owner_id != current_user.user_id: 
        raise utils.ForbiddenException(msg="Not authorized to perform requested action")
    
    results = database.updateItemById(**{
        "table": models.Post,
        "item_id": post_id,
        "set_values": {
            "likes": post.likes + (1 - dislike*2)
        }
    }, session=db)

    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )

    return results

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(post_id: int, 
    current_user: schemas.TokenData = Depends(authorized_users), db: Session = Depends(connection)
):
    post = __get_post(post_id, db)
    
    if post.owner_id != current_user.user_id: 
        raise utils.ForbiddenException(msg="Not authorized to perform requested action")
    
    results = database.deleteItemById(
        table=models.Post,item_id=post_id, session=db
    )
    
    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
    
    return 

def __get_post(post_id: int, db: Session = Depends(connection)) -> schemas.PostDisplayView:
    results = database.readItemById(
        table=models.Post, item_id=post_id, session=db
    )
    
    if not results:
        raise utils.notFoundException(
            msg=f"Post with post_id={post_id} does not exists or ID our of range"
        )
        
    return results

