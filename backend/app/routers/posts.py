from fastapi import APIRouter, Depends, Security, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select, or_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user_model import User
from app.models.post_model import Post, PostCreate, PostPublicWithUser
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.post("/", response_model=PostPublicWithUser)
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

@router.get("/", response_model=List[PostPublicWithUser])
def read_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1)
):
    """
    Retrieve posts. If a query 'q' is provided, it filters posts 
    by title and content. Otherwise, it returns all posts.
    """
    statement = select(Post).options(selectinload(Post.user))
    if q:
        # Case-insensitive search for the query in title or content
        statement = statement.where(or_(Post.title.ilike(f"%{q}%"), Post.content.ilike(f"%{q}%")))

    posts = db.exec(select(Post)).all()
    return posts

@router.get("/{post_id}", response_model=PostPublicWithUser)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    post = db.exec(statement).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post