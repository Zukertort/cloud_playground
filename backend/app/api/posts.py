from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PostBase(BaseModel):
    post_id: int
    title: str
    content: str
    author_id: int
    published_date: datetime

@app.get("/")
async def all_posts():
    return {"message": "Welcome to my API"}

@app.get("/posts")
async def all_posts():
    return {"message": "All posts"}

@app.get("/posts/{post_name}")
async def get_post(post: PostBase):
    return {"post_id": post.post_id, "title": post.title, "content": post.content, "author_id": post.author_id, "published_date": post.published_date}