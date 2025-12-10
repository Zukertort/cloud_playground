from fastapi import APIRouter, Depends, Security, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select, or_, func, desc
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user_model import User
from app.models.post_model import Post, PostCreate, PostPublicWithUser, PaginatedPosts, PostTitleAndDate
from app.dependencies import get_current_user

# Current admin ID
Admin = 1

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)
# CREATE A POST
@router.post("/", response_model=PostPublicWithUser)
def create_post(
    post_data: PostCreate,
    current_user: User = Security(get_current_user),
    db: Session = Depends(get_db)
):
    new_post = Post.model_validate(post_data, update={"user_id": current_user.id})
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# READ ALL POSTS
@router.get("/", response_model=PaginatedPosts)
def read_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1),
    offset: int = 0,
    limit: int = 5
):
    """
    Retrieve posts with sorting and pagination.
    - Posts are sorted from newest to oldest.
    - If a query 'q' is provided, it filters posts by title and content.
    - 'offset' is the number of items to skip.
    - 'limit' is the maximum number of items to return.
    """
    statement = select(Post).options(selectinload(Post.user))
    if q:
        search_query = q.lower()
        statement = statement.where(or_(
            func.lower(Post.title).contains(search_query),
            func.lower(Post.content).contains(search_query)
        ))

    # Get the total count of posts matching the filter
    count_statement = select(func.count()).select_from(statement.subquery())
    total_count = db.exec(count_statement).one()

    # Get the paginated and sorted posts
    posts_statement = statement.order_by(Post.created_at.desc()).offset(offset).limit(limit)
    posts = db.exec(posts_statement).all()
    
    return {"total": total_count, "posts": posts}

# READ A POST
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

# LIST POSTS BY USER
@router.get("/user/{user_id}", response_model=List[PostTitleAndDate])
def read_posts_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != Admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this user's posts")
    
    statement = select(Post).where(Post.user_id == user_id)
    posts = db.exec(statement).all()

    if not posts and user_id != current_user.id:
        user_exists = db.get(User, user_id)
        if not user_exists:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        
    return posts

# UPDATE A POST
@router.put("/{post_id}", response_model=PostPublicWithUser)
async def update_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    if not any(post.id == post_id for post in current_user.posts):
        raise HTTPException(status_code=403, detail="You do not have permission to update this post")
    statement = select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    post = db.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post