from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime


PhoneStr = Annotated[str, StringConstraints(min_length=10, max_length=15)]

class UserCreate(BaseModel):
    full_name: str
    phone_number: str  # Keep simple str if not using PhoneStr validator
    password: str
    role: str  # "admin" or "customer"

    # Optional fields
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    notes: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str
