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
    prefix="/users",
    tags=["Users"]
)

### Operation on Users

@router.post("/", 
             status_code=status.HTTP_201_CREATED, response_model=views.UserInfo)
def create_user(payload: schemas.User, db: Session = Depends(connection)):
    hashed_pwd = utils.hashPassword(payload.input_pwd)
    
    results = database.createItem(
        table=models.User,
        item=payload.dict(exclude={"input_pwd"}) | {"hashed_pwd": hashed_pwd}, 
        session=db
    )
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{
                "msg": f"Post creation fail"
            }],           
        )

    return results
### Helper Functions

@router.get("/{user_id}", response_model=views.UserInfo)
def read_user(user_id: int, db: Session = Depends(connection)):
    # validateAndGetPost(post_id)
    results = database.readItemById(
        table=models.User, item_id=user_id, session=db
    )
    
    if not results:
        raise utils.notFoundException(
            msg=f"User with user_id={user_id} does not exists or ID our of range"
        )
    
    return results