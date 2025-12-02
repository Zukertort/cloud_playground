from typing import Annotated
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class HeroBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    mail: str | None = None
    create_at: datetime | None = None
    password_hash: str