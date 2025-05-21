from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Booking, GroupMember, Payment
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

    # Daily total revenue
    daily_total = db.query(func.sum(Payment.payment_amount)).filter(
        Payment.payment_status == "completed",
        Payment.is_deleted == False,
        func.date(Payment.payment_date) == today
    ).scalar()

    # Weekly total revenue
    weekly_total = db.query(func.sum(Payment.payment_amount)).filter(
        Payment.payment_status == "completed",
        Payment.is_deleted == False,
        func.date(Payment.payment_date) >= start_of_week
    ).scalar()

    # Monthly total revenue
    monthly_total = db.query(func.sum(Payment.payment_amount)).filter(
        Payment.payment_status == "completed",
        Payment.is_deleted == False,
        func.date(Payment.payment_date) >= start_of_month
    ).scalar()

    # Total bookings today (with completed payments)
    todays_bookings = db.query(func.count()).filter(
        Payment.payment_status == "completed",
        Payment.is_deleted == False,
        func.date(Payment.payment_date) == today
    ).scalar()

    return {
        "todays_bookings": todays_bookings,
        "revenue_today": float(daily_total or 0),
        "revenue_week": float(weekly_total or 0),
        "revenue_month": float(monthly_total or 0)
    }

