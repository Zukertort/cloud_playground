from pydantic import BaseModel, EmailStr

# Properties to receive via API on user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Properties to return to client
class UserPublic(BaseModel):
    id: int
    email: EmailStr

# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str

# Data in the token
class TokenData(BaseModel):
    email: str = None