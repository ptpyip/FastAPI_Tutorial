
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class BaseSchema(BaseModel):
    pass

class Post(BaseSchema):
    title: str
    content: str
    is_published: bool = True
    
class PostResponse(Post):
    '''
        A response model for post
    '''
    id: int
    likes: int
    content: str
    
    class Config:
        orm_mode = True
    
class User(BaseSchema):
    email: EmailStr
    hashed_pwd: str
    
class UserIn(BaseSchema):
    email: EmailStr
    hashed_pwd: str
    display_name: str
    url_to_display_img: Optional[str] = None
    
class Userout(BaseSchema):
    email: EmailStr
    display_name: str
    url_to_display_img: Optional[str] = None
    
    class Config:
        orm_mode = True
    
    
    
    