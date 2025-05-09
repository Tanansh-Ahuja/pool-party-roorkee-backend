<<<<<<< HEAD
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Booking, GroupMember
from datetime import date

def get_total_earnings_for_date(db: Session, target_date: date):
    booking_total = db.query(func.sum(Booking.total_amount))\
        .filter(Booking.booking_date == target_date, Booking.deleted == False)\
        .scalar() or 0

    rental_total = db.query(
        func.sum(GroupMember.swimwear_cost + GroupMember.tube_cost +
                 GroupMember.cap_cost + GroupMember.goggles_cost)
    ).join(Booking).filter(Booking.booking_date == target_date, Booking.deleted == False)\
     .scalar() or 0

    return {
        "date": target_date,
        "booking_total": float(booking_total),
        "rental_total": float(rental_total),
        "total_earnings": float(booking_total + rental_total)
    }
=======
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Booking, GroupMember
from datetime import date

def get_total_earnings_for_date(db: Session, target_date: date):
    booking_total = db.query(func.sum(Booking.total_amount))\
        .filter(Booking.booking_date == target_date, Booking.deleted == False)\
        .scalar() or 0

    rental_total = db.query(
        func.sum(GroupMember.swimwear_cost + GroupMember.tube_cost +
                 GroupMember.cap_cost + GroupMember.goggles_cost)
    ).join(Booking).filter(Booking.booking_date == target_date, Booking.deleted == False)\
     .scalar() or 0

    return {
        "date": target_date,
        "booking_total": float(booking_total),
        "rental_total": float(rental_total),
        "total_earnings": float(booking_total + rental_total)
    }
>>>>>>> origin/main
