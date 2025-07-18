from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    created_at: str
    password_hash: str