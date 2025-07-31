from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_model import User, UserPublic

class PostBase(SQLModel):
    title: str
    content: str

class Post(PostBase, table=True):
    # Table name
    __tablename__ = "posts"
    # Schema
    __table_args__ = {"schema": "cpg"}

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Foreign key relationship to the 'users' table
    user_id: int = Field(foreign_key="cpg.users.id")
    
    # The Relationship attribute links this model to the User model
    # It allows you to access the related user object, e.g., my_post.user
    user: "User" = Relationship(back_populates="posts")

# API model for creating a post (doesn't include id, created_at, or user_id)
class PostCreate(PostBase):
    pass

# API model for reading a post (includes id and created_at)
class PostPublic(PostBase):
    id: int
    created_at: datetime

# API model for reading a post that also includes the owner's public info
class PostPublicWithUser(PostPublic):
    user: "UserPublic"