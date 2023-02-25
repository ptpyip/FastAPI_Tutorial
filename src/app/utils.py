from fastapi import HTTPException, status
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(pwd: str):
    return pwd_context.hash(pwd)

### Helper functions

def notFoundException(msg): 
    """ return Not Found Exception to client side"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{
            "loc": [
                "path",
                "id"
            ],
            "msg": msg
        }],           
    )