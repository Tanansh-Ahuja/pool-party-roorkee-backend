from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Booking, GroupMember, Payment
from datetime import date, timedelta

def get_total_earnings_for_date(db: Session, payment_date: date):
    result = db.query(
        func.coalesce(func.sum(Payment.swimming_amount), 0).label("swimming_revenue"),
        func.coalesce(func.sum(Payment.rental_amount), 0).label("rental_revenue"),
        func.coalesce(func.sum(Payment.payment_amount), 0).label("total_revenue")
    ).filter(
        func.date(Payment.payment_date) == payment_date,
        Payment.payment_status == "completed",
        Payment.is_deleted == False
    ).one()

    return {
        "swimming_revenue": float(result.swimming_revenue),
        "rental_revenue": float(result.rental_revenue),
        "total_revenue": float(result.total_revenue)
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

