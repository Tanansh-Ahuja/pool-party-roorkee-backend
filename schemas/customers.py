from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated
from datetime import datetime

PhoneStr = Annotated[str, StringConstraints(min_length=10, max_length=15)]

class CustomerBase(BaseModel):
    full_name: str
    phone_number: PhoneStr
    gender: Optional[str] = None
    age: Optional[int] = None
    swimming_minutes: Optional[int] = None
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUserUpdate(BaseModel):
    # User fields
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    # Customer fields
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True

class CustomerOut(CustomerBase):
    customer_id: int
    registered_at: datetime
    swimming_minutes: Optional[int]

    class Config:
        from_attributes = True

class CustomerProfileOut(BaseModel):
    customer_id: int
    full_name: str
    phone_number: str
    gender: Optional[str]
    age: Optional[int]
    swimming_minutes: Optional[int]
    registered_at: datetime
    username: Optional[str]
    email: Optional[str]
    role: str

    class Config:
        from_attributes = True
