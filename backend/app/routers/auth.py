from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_db
from app.models.user_model import User, UserCreate, UserPublic
from app.security import get_password_hash, verify_password, create_access_token
from app.schemas import Token
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserPublic)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
        
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User.model_validate(
        user_data,
        update={
            "password_hash": hashed_password,
        }
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user