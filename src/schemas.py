
from typing import Optional
from pydantic import BaseModel
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
    
    