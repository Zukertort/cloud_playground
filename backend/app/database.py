import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the connection")

engine = create_engine(DATABASE_URL, echo=True) # echo=True for dev logging

def get_db():
    with Session(engine) as session:
        yield session