from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime


PhoneStr = Annotated[str, StringConstraints(min_length=10, max_length=15)]

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # "admin" or "customer"

     # Customer-specific fields
    full_name: str
    phone_number: PhoneStr
    gender: Optional[str] = None
    age: Optional[int] = None
    swimming_minutes: Optional[int] = None
    notes: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
