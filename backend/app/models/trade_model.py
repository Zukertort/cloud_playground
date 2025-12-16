from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class Trade(SQLModel, table=True):
    __tablename__ = "trades"
    __table_args__ = {"schema": "cpg"}

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="cpg.users.id")
    
    ticker: str
    side: str
    quantity: int
    price: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    status: str = "EXECUTED"