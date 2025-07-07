import json as js
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path

app = FastAPI()

# Allowed origins
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add the CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_file_path = Path(__file__).parent.parent / "tests" / "data.json"

class PostBase(BaseModel):
    post_id: int
    title: str
    content: str
    author_id: int
    published_date: datetime

# This is loaded once at startup. For a real app, this would be a database connection.
all_blog_posts: Dict[int, PostBase] = {}

def load_posts_from_json(file_path: str) -> Dict[int, PostBase]:
    """Loads a list of posts from a JSON file and returns them as a dictionary keyed by post_id."""
    try:
        with open(file_path, 'r') as f:
            raw_data = js.load(f)
        if not isinstance(raw_data, list):
            raise ValueError("Error loading data: Expected a json file.")

        posts_dict = {}
        for item in raw_data:
            try:
                post = PostBase(**item)
                posts_dict[post.post_id] = post
            except Exception as e:
                print(f"Error parsing post data: {item}. Error: {e}")
        return posts_dict
    
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}. No posts loaded.")
        return {}
    
    except js.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}. Check file format.")
        return {}
    
    except ValueError as e:
        print(f"Error: {e}")
        return {}
    
# Load posts when the application starts
all_blog_posts = load_posts_from_json(data_file_path)
if not all_blog_posts:
    print("Warning: No posts were loaded.")

# API endpoints
@app.get("/")
async def all_posts():
    return {"message": "Welcome to my API"}

@app.get("/posts")
async def get_all_posts(skip: int = 0, limit: int = 5):
    """
    Retrieve a paginated list of posts.
    - 'skip': number of posts to skip
    - 'limit': maximum number of posts to return
    """
    
    posts_list = list(all_blog_posts.values())

    return posts_list[skip : skip + limit]


@app.get("/posts/{post_id}", response_model=PostBase)
async def get_single_post(post_id: int):
    """Retrieve a single post by its ID."""

    post = all_blog_posts.get(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@app.post("/posts/", response_model=PostBase, status_code=201)
async def create_post(post: PostBase):
    """Create a new post."""

    if post.post_id in all_blog_posts:
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    all_blog_posts[post.post_id] = post

    # Just for testing. In a real app, you'd save this to a database
    return post