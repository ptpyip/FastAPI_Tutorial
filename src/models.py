from typing import List, Optional
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import types 

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    pass

class Post(BaseModel):
    __tablename__ = "Posts"
    
    title: Mapped[str]
    created_at = Column(types.TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())
    is_published: Mapped[bool] = mapped_column(server_default='TRUE')
    likes: Mapped[int] = mapped_column(server_default='0')
    content:Mapped[Optional[str]]       # Optional -> implies nullable
    
    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, is_published={self.is_published!r}, likes={self.likes!r}, content={self.content!r})"

    # def getDict(self):
    #     return  {
    #         "post_id": self.post_id,
    #         "title": self.title,
    #         "is_publised": self.is_publised,
    #         "likes": self.likes,
    #         "content": self.content
    #     }