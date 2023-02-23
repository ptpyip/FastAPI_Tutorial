
from typing import Optional
from pydantic import BaseModel

class BaseSchema(BaseModel):
    pass

class Post(BaseSchema):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None
    