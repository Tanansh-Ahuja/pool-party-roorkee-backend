from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Booking, GroupMember
from datetime import date, timedelta

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

def get_summary(db):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_of_month = today.replace(day=1)

    # Bookings today
    todays_bookings = db.query(Booking).filter(
        Booking.booking_date == today,
        Booking.deleted == False
    ).count()

    # Revenue Today
    revenue_today = get_total_earnings_for_date(db, today)["total_earnings"]

    # Revenue This Week
    revenue_week = _get_earnings_for_range(db, start_of_week, today)

    # Revenue This Month
    revenue_month = _get_earnings_for_range(db, start_of_month, today)

    return {
        "todays_bookings": todays_bookings,
        "revenue_today": revenue_today,
        "revenue_week": revenue_week,
        "revenue_month": revenue_month
    }

def _get_earnings_for_range(db: Session, start_date: date, end_date: date):
    booking_total = db.query(func.sum(Booking.total_amount)).filter(
        Booking.booking_date >= start_date,
        Booking.booking_date <= end_date,
        Booking.deleted == False
    ).scalar() or 0

    rental_total = db.query(
        func.sum(
            GroupMember.swimwear_cost + GroupMember.tube_cost +
            GroupMember.cap_cost + GroupMember.goggles_cost
        )
    ).join(Booking).filter(
        Booking.booking_date >= start_date,
        Booking.booking_date <= end_date,
        Booking.deleted == False
    ).scalar() or 0

    return float(booking_total + rental_total)

