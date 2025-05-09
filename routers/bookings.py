<<<<<<< HEAD
from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.bookings import BookingCreate, BookingOut, CustomerbookingOut
from schemas.group_members import GroupMemberCreate

from crud.bookings import create_booking, get_booking, get_all_bookings, create_booking_with_members, mark_booking_as_paid, cancel_booking
from crud.bookings import update_booking, delete_booking, get_bookings_for_date, get_all_bookings_of_customer,get_revenue_for_date
import crud.settings as crud_settings

from utils.auth import get_current_user
from models import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut)
def create_booking_route(booking: BookingCreate, db: Session = Depends(get_db)):
    if not crud_settings.is_booking_enabled(db):
        raise HTTPException(status_code=403, detail="Online bookings are currently disabled.")
    return create_booking(db, booking)

@router.post("/CustomerCreateBooking", response_model=BookingOut)
def create_booking_route(
    group_members: List[GroupMemberCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not crud_settings.is_booking_enabled(db):
        raise HTTPException(status_code=403, detail="Online bookings are currently disabled.")
    
    booking = create_booking_with_members(db, current_user.user_id, group_members)
    return booking

@router.get("/", response_model=list[BookingOut])
def read_all_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@router.get("/customer/me", response_model=List[CustomerbookingOut])
def get_customer_bookings(current_user: User = Depends(get_current_user),db: Session = Depends(get_db),skip: int = 0,limit: int = 10):
    return get_all_bookings_of_customer(current_user.user_id,db,skip,limit)

@router.get("/revenue/{booking_date}")
def get_daily_revenue(booking_date: date, db: Session = Depends(get_db)):
    return get_revenue_for_date(db, booking_date)

@router.patch("/mark-paid/{booking_id}", response_model=BookingOut)
def mark_paid(booking_id: int, db: Session = Depends(get_db)):
    return mark_booking_as_paid(db, booking_id)

@router.patch("/cancel/{booking_id}", response_model=BookingOut)
def cancel(booking_id: int, db: Session = Depends(get_db)):
    return cancel_booking(db, booking_id)


@router.get("/by-date/{booking_date}", response_model=list[BookingOut])
def get_bookings_by_date(booking_date: date, db: Session = Depends(get_db)):
    return get_bookings_for_date(db, booking_date)

@router.get("/{booking_id}", response_model=BookingOut)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking_route(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, booking)

@router.delete("/{booking_id}")
def delete_booking_route(booking_id: int, db: Session = Depends(get_db)):
    return delete_booking(db, booking_id)
=======
from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.bookings import BookingCreate, BookingOut, CustomerbookingOut
from schemas.group_members import GroupMemberCreate

from crud.bookings import create_booking, get_booking, get_all_bookings, create_booking_with_members, mark_booking_as_paid, cancel_booking
from crud.bookings import update_booking, delete_booking, get_bookings_for_date, get_all_bookings_of_customer,get_revenue_for_date
import crud.settings as crud_settings

from utils.auth import get_current_user
from models import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut)
def create_booking_route(booking: BookingCreate, db: Session = Depends(get_db)):
    if not crud_settings.is_booking_enabled(db):
        raise HTTPException(status_code=403, detail="Online bookings are currently disabled.")
    return create_booking(db, booking)

@router.post("/CustomerCreateBooking", response_model=BookingOut)
def create_booking_route(
    group_members: List[GroupMemberCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not crud_settings.is_booking_enabled(db):
        raise HTTPException(status_code=403, detail="Online bookings are currently disabled.")
    
    booking = create_booking_with_members(db, current_user.user_id, group_members)
    return booking

@router.get("/", response_model=list[BookingOut])
def read_all_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@router.get("/customer/me", response_model=List[CustomerbookingOut])
def get_customer_bookings(current_user: User = Depends(get_current_user),db: Session = Depends(get_db),skip: int = 0,limit: int = 10):
    return get_all_bookings_of_customer(current_user.user_id,db,skip,limit)

@router.get("/revenue/{booking_date}")
def get_daily_revenue(booking_date: date, db: Session = Depends(get_db)):
    return get_revenue_for_date(db, booking_date)

@router.patch("/mark-paid/{booking_id}", response_model=BookingOut)
def mark_paid(booking_id: int, db: Session = Depends(get_db)):
    return mark_booking_as_paid(db, booking_id)

@router.patch("/cancel/{booking_id}", response_model=BookingOut)
def cancel(booking_id: int, db: Session = Depends(get_db)):
    return cancel_booking(db, booking_id)


@router.get("/by-date/{booking_date}", response_model=list[BookingOut])
def get_bookings_by_date(booking_date: date, db: Session = Depends(get_db)):
    return get_bookings_for_date(db, booking_date)

@router.get("/{booking_id}", response_model=BookingOut)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking_route(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, booking)

@router.delete("/{booking_id}")
def delete_booking_route(booking_id: int, db: Session = Depends(get_db)):
    return delete_booking(db, booking_id)
>>>>>>> origin/main
