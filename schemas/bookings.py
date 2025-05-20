from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated, List
from datetime import datetime, date, time

TextStr = Annotated[str, StringConstraints(max_length=500)]

class BookingBase(BaseModel):
    customer_id: int
    booking_time: Optional[datetime]
    booking_date: date
    slot_start: time
    slot_end: time
    number_of_people: int
    food_order: Optional[TextStr] = None
    total_amount: float
    payment_status: Optional[str] = "pending"
    band_color: Optional[str] = None
    
class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    booking_time: Optional[datetime]
    booking_date: Optional[date]
    slot_start: Optional[time]
    slot_end: Optional[time]
    number_of_people: Optional[int]
    food_order: Optional[TextStr]
    total_amount: Optional[float]
    payment_status: Optional[str]
    band_color: Optional[str]
    deleted: Optional[bool]

class UnpaidBookingOut(BaseModel):
    booking_id: int
    booking_date: Optional[date]=None
    slot_start: Optional[time]=None
    slot_end: Optional[time]=None
    total_amount: Optional[float]=None
    customer_name: Optional[str]=None

    class Config:
        from_attributes = True


class BookingOut(BookingBase):
    booking_id: int
    booking_time: Optional[datetime]
    customer_name: Optional[str] = None
    deleted: bool

    class Config:
        from_attributes = True

class CustomerbookingOut(BookingBase):
    booking_id: int
    booking_time: Optional[datetime]
    deleted: bool
    rental_total: Optional[int]

    class Config:
        from_attributes = True
