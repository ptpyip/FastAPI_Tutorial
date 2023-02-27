from typing import List, Optional
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Relationship
from sqlalchemy import func
from sqlalchemy import types 

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

class Post(BaseModel):
    __tablename__ = "Posts"
    
    title: Mapped[str]
    created_at = Column(types.TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())
    is_published: Mapped[bool] = mapped_column(server_default='TRUE')
    likes: Mapped[int] = mapped_column(server_default='0')
    content:Mapped[Optional[str]]       # Optional -> implies nullable
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = Relationship(back_populates="User")
    
    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, is_published={self.is_published!r}, likes={self.likes!r}, content={self.content!r})"

class User(BaseModel):
    __tablename__ = "Users"
    
    email: Mapped[str] = mapped_column(unique=True)
    hashed_pwd: Mapped[str]
    display_name: Mapped[str]
    url_to_display_img: Mapped[Optional[str]]
    created_at = Column(types.TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())
    
    posts: Mapped["User"] = Relationship(back_populates="Post")
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, hashed_pwd={self.hashed_pwd!r}, display_name={self.display_name!r}, created_at={self.created_at!r})"

    
    
    