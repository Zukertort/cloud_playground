from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import datetime, timezone
from typing import List



class Strategy(SQLModel, table=True):
    __tablename__ = "strategies"
    __table_args__ = {"schema": "cpg"}
    id: int = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="cpg.users.id")
    name: Optional[str] = Field(default=None, index=True)
    code_logic: str = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
