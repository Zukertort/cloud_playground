from pydantic import BaseModel, Field, EmailStr, ValidationError
from datetime import datetime

class CreditCard(BaseModel):
    card_number: int
    expiration_date: datetime = Field(default_factory=datetime.now)
    security_code: int

class Client(BaseModel):
    name: str
    age: int
    email: EmailStr
    payment_information: CreditCard | None = None