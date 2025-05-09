from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    booking_id: int
    payment_date: datetime
    payment_amount: float
    swimming_amount: Optional[float] = None
    rental_amount: Optional[float] = None
    payment_method: str
    payment_status: str
    transaction_id: str
    notes: Optional[str] = None
    is_deleted: bool = False

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    payment_status: Optional[str]
    transaction_id: Optional[str]
    is_deleted: Optional[bool]

class PaymentOut(PaymentBase):
    class Config:
        from_attributes = True
