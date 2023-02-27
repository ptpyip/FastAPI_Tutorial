from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
from app import database, utils, security

from config import FASTAPI_TUT_DATABASE_URL
from ..security import OAuth

### Initialization
connection =  database.Connection(FASTAPI_TUT_DATABASE_URL)

authorized_user = security.AuthorizedUser()

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(connection)):
    # OAuth2PasswordRequestForm -> form_data
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    # token = "example token"
    token = OAuth.createAccessToken(data={
        "user_id": user.id,
        "display_name" :user.display_name
    })
    return {"access_token": token, "token_type": "bearer"}
    
def authenticateUser(username: str, password: str, session: Session):
    user = database.readItem(
        table=models.User,
        filters=[
            models.User.email == username
        ],
        session=session
    )
    
    if not user or not security.verify(password, user.hashed_pwd):
        return False
    
    return user