from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

### Model Schema
class BaseSchema(BaseModel):
    pass

class Post(BaseSchema):
    title: str
    content: str
    is_published: bool = True

class UserCreate(BaseSchema):
    email: EmailStr
    input_pwd: str
    display_name: str
    url_to_display_img: Optional[str] = None
            
class UserLogin(BaseSchema):
    email: EmailStr
    input_pwd: str

### View Schema
class BaseView(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)    # set default value to datetime.now()
    
    class Config:
        orm_mode = True
        
class UserInfoView(BaseView):
    id: int
    email: EmailStr
    display_name: str
    url_to_display_img: Optional[str] = None  
       
class PostDisplayView(BaseView):
    '''
        A response model for post
    '''
    id: int
    owner: UserInfoView
    title: str
    likes: int
    is_published: bool = True
    content: str
            
class UserProfile(UserInfoView):
    posts: List[PostDisplayView]
             
### Token Schema
class Token(BaseSchema):
    access_token: str
    token_type: str
    
class TokenData(BaseSchema):
    user_id: str
    display_name: str