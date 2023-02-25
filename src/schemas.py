
from typing import Optional
from pydantic import BaseModel, EmailStr

class BaseSchema(BaseModel):
    pass

class Post(BaseSchema):
    title: str
    content: str
    is_published: bool = True

class User(BaseSchema):
    email: EmailStr
    input_pwd: str
    display_name: str
    url_to_display_img: Optional[str] = None
            