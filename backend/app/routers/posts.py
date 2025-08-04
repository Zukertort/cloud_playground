from fastapi import APIRouter, Depends, Security, HTTPException
from typing import List
from sqlmodel import Session, select

from app.database import get_db
from app.models.user_model import User
from app.models.post_model import Post, PostCreate, PostPublic
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.post("/", response_model=PostPublic)
def create_post(
    post_data: PostCreate,
    current_user: User = Security(get_current_user),
    db: Session = Depends(get_db)
):
    # Create a new Post instance, associating it with the current user
    new_post = Post.model_validate(post_data, update={"user_id": current_user.id})
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[PostPublic])
def read_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all posts.
    """
    posts = db.exec(select(Post)).all()
    return posts

@router.get("/{post_id}", response_model=PostPublic)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post