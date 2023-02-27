
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session


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
    
def ForbiddenException(msg, headers=None): 
    """ return Not Found Exception to client side"""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg,    
        headers=headers      
    )