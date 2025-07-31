from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .post_model import Post

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)

class User(SQLModel, table=True):
    # Table name
    __tablename__ = "users"
    # Schema
    __table_args__ = {"schema": "cpg"}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    password_hash: str
    posts: List["Post"] = Relationship(back_populates="user")

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserPublic(SQLModel):
    id: int
    username: str
    # email: str