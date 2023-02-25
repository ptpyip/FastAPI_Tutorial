
'''
- This module contains pydantic models repersent a view to the database
- for response model used in FastAPI 
'''


from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class BaseView(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)    # set default value to datetime.now()
    
    class Config:
        orm_mode = True
        
class PostDisplay(BaseView):
    '''
        A response model for post
    '''
    id: int
    likes: int
    content: str
    
class UserInfo(BaseView):
    id: int
    email: EmailStr
    display_name: str
    url_to_display_img: Optional[str] = None
    