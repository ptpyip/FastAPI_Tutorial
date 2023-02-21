from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

import Models.Base as Base

class Post(Base):
    __tablename__ = "Posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    is_published: Mapped[bool] = mapped_column(default=True)
    likes: Mapped[int] = mapped_column(default=0)
    content:Mapped[Optional[str]]
    
    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, is_published={self.is_published!r}, likes={self.likes!r}, content={self.content!r})"
