from pydantic import BaseModel

# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str

# Data in the token
class TokenData(BaseModel):
    username: str