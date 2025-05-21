import random
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Payment
from schemas.payments import PaymentCreate, PaymentUpdate

def create_payment(db: Session, rental_total,swimming_amount,new_booking):
    payment_amount = swimming_amount + rental_total
    # Create Payment row
    new_payment = Payment(
        booking_id=new_booking.booking_id,
        payment_amount=payment_amount,
        swimming_amount=swimming_amount,
        rental_amount=rental_total,
        payment_method="pending",  # or "not selected yet"
        payment_status="pending",
        transaction_id=f"txn_{new_booking.booking_id}_{random.randint(1000, 9999)}",  # temporary unique ID
        notes="Auto-generated on booking creation",
        is_deleted=False
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()

def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()

def update_payment(db: Session, payment_id: int, payment: PaymentUpdate):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment:
        for key, value in payment.dict(exclude_unset=True).items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    return None

def get_daily_revenue_data(db: Session):
    results = (
        db.query(
            func.date(Payment.payment_date).label("payment_day"),
            func.coalesce(func.sum(Payment.swimming_amount), 0).label("swimming_total"),
            func.coalesce(func.sum(Payment.rental_amount), 0).label("rental_total"),
            func.coalesce(func.sum(Payment.payment_amount), 0).label("total_revenue")
        )
        .filter(Payment.is_deleted == False)
        .filter(Payment.payment_status == "completed")
        .group_by(func.date(Payment.payment_date))
        .order_by(func.date(Payment.payment_date))
        .all()
    )

    labels = []
    swimming_ticket = []
    rental = []
    total = []

    for row in results:
        labels.append(row.payment_day.strftime('%Y-%m-%d'))
        swimming_ticket.append(float(row.swimming_total))
        rental.append(float(row.rental_total))
        total.append(float(row.total_revenue))

    return {
        "labels": labels,
        "swimming_ticket": swimming_ticket,
        "rental": rental,
        "total": total
    }