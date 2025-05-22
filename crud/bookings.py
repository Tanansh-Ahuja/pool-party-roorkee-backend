from datetime import date, datetime
import random
from typing import List
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Booking, GroupMember, Customer, Payment
from schemas.group_members import GroupMemberCreate
from schemas.bookings import BookingOut
from utils.get_customer_id_from_user import get_customer_id_from_user_id
from crud.group_members import create_group_members
from crud.payments import create_payment

def _updating_swimming_minutes_for_booking(db,booking,booking_id):
    # 2. Calculate duration in minutes
    try:
        slot_start_dt = datetime.combine(date.today(), booking.slot_start)
        slot_end_dt = datetime.combine(date.today(), booking.slot_end)
        duration_minutes = int((slot_end_dt - slot_start_dt).total_seconds() // 60)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid slot time format: {e}")
    
    try:
        # 3. Fetch all customer_ids from group_members of this booking
        group_members = db.query(GroupMember).filter(GroupMember.booking_id == booking_id).all()
        customer_ids = {member.customer_id for member in group_members if member.customer_id is not None}
        customer_ids = list(set(customer_ids))

        # 4. Update swimming_minutes in customer table
        for customer_id in customer_ids:
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            if customer:
                customer.swimming_minutes = (customer.swimming_minutes or 0) + duration_minutes
    except Exception as e:
        raise Exception(detail=f"{e}")
    db.commit()

def _marking_payment_row_of_booking_as_paid(db,booking_id):
    # Fetch corresponding payment
    payment = db.query(Payment).filter(Payment.booking_id == booking_id, Payment.is_deleted == False).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Associated payment not found")

    # Update payment fields
    payment.payment_status = "completed"
    payment.payment_method = "cash"
    payment.payment_date = datetime.now()  # override in case payment was generated earlier

    db.commit()
    db.refresh(payment)

def get_all_bookings_of_customer(user_id: int, db, skip: int = 0, limit: int = 10):
    # Step 1: Get customer_id from user_id
    customer = db.query(Customer).filter(Customer.user_id == user_id).first()
    if not customer:
        return []

    customer_id = customer.customer_id

    # Step 2: Get all booking IDs where the customer is either a booker or a group member
    group_booking_ids = db.query(GroupMember.booking_id).filter(
        GroupMember.customer_id == customer_id
    ).distinct().all()
    group_booking_ids = [row[0] for row in group_booking_ids]

    own_booking_ids = db.query(Booking.booking_id).filter(
        Booking.customer_id == customer_id
    ).all()
    own_booking_ids = [row[0] for row in own_booking_ids]

    all_booking_ids = list(set(group_booking_ids + own_booking_ids))

    # Step 3: Fetch bookings with pagination
    bookings = db.query(Booking).filter(
        Booking.booking_id.in_(all_booking_ids), Booking.deleted == False
    ).order_by(Booking.booking_date.desc()).offset(skip).limit(limit).all()

    result = []
    for booking in bookings:
        # Step 4: Get rental total for this booking from group_members
        rental_total = db.query(
            func.coalesce(func.sum(GroupMember.swimwear_cost), 0) +
            func.coalesce(func.sum(GroupMember.tube_cost), 0) +
            func.coalesce(func.sum(GroupMember.cap_cost), 0)+
            func.coalesce(func.sum(GroupMember.goggles_cost), 0)
        ).filter(GroupMember.booking_id == booking.booking_id).scalar()

        # Step 5: Add rental_total to booking dictionary
        booking_dict = booking.__dict__.copy()
        booking_dict["rental_total"] = rental_total

        # Optionally, remove SQLAlchemy internal fields
        booking_dict.pop("_sa_instance_state", None)

        result.append(booking_dict)

    return result

def create_booking_with_members(db, user_id: int, members_data: List[GroupMemberCreate]):
    if not members_data:
        raise HTTPException(status_code=400, detail="No group members provided.")

    # Use the first member's timing for booking
    first_member = members_data[0]
    slot_start = first_member.slot_start
    slot_end = first_member.slot_end
    # Convert times into datetime objects on a dummy date to find the difference
    dummy_date = datetime(2025, 1, 1)  # any date is fine
    start_datetime = datetime.combine(dummy_date, slot_start)
    end_datetime = datetime.combine(dummy_date, slot_end)

    # Calculate the time difference
    duration = end_datetime - start_datetime
    minutes = duration.total_seconds() / 60  # convert seconds to minutes

    # Price calculation
    price_per_minute = 5 / 3  # as per your logic
    amount_per_person = round(minutes * price_per_minute)
    final_band_color = random.choice(['red','green','yellow','white','blue','grey'])
    # Create the booking
    new_booking = Booking(
        customer_id = get_customer_id_from_user_id(db, user_id),  # you will create this function
        booking_date = first_member.booking_date,
        slot_start = first_member.slot_start,
        slot_end = first_member.slot_end,
        number_of_people = len(members_data),
        total_amount = len(members_data)*amount_per_person,  # we'll calculate below
        payment_status = "pending",
        band_color = final_band_color,
        deleted = False
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    # After creating the booking
    rental_total = create_group_members(db, members_data, new_booking, amount_per_person)
    # Swimming and rental totals
    swimming_amount = len(members_data) * amount_per_person
    create_payment(db,rental_total,swimming_amount,new_booking)
    return new_booking

def get_all_bookings(db: Session):
    return db.query(Booking).all()

def get_overstayed_bookings(db: Session, booking_date: date):
    now = datetime.now().time()

    bookings = db.query(Booking).filter(
        Booking.booking_date == booking_date,
        Booking.slot_end < now,
        Booking.payment_status == "paid",
        Booking.in_pool == True,
        Booking.deleted == False
    ).all()

    result = []
    for booking in bookings:
        customer = db.query(Customer).filter(Customer.customer_id == booking.customer_id).first()
        result.append({
            "booking_id": booking.booking_id,
            "booking_date": booking.booking_date,
            "slot_start": booking.slot_start,
            "slot_end": booking.slot_end,
            "customer_name": customer.full_name if customer else "Unknown"
        })

    return result

def get_bookings_for_date(db: Session, booking_date: date):
    bookings = (
        db.query(Booking)
        .filter(Booking.booking_date == booking_date, Booking.deleted == False)
        .all()
    )

    output = []
    for booking in bookings:

        payment = db.query(Payment.payment_amount).filter(Payment.booking_id == booking.booking_id).first()
        booking.total_amount = float(payment[0])

        # Get group members for that booking
        group_members = (
            db.query(GroupMember.full_name)
            .filter(GroupMember.booking_id == booking.booking_id)
            .all()
        )

        # Flatten group member names
        member_names = [gm.full_name for gm in group_members]

        all_names = member_names

        # Convert booking to dict and add all_names
        b_dict = booking.__dict__.copy()
        b_dict["all_names"] = all_names

        # Remove private fields if necessary
        b_dict.pop("_sa_instance_state", None)

        output.append(BookingOut(**b_dict))

    return output

def get_bookings_today_unpaid(db: Session, booking_date: date):
    results = (
        db.query(
            Booking.booking_id,
            Booking.booking_date,
            Booking.slot_start,
            Booking.slot_end,
            Booking.total_amount,
            Customer.full_name.label("customer_name")
        )
        .join(Customer, Booking.customer_id == Customer.customer_id)
        .filter(
            Booking.booking_date == booking_date,
            Booking.deleted == False,
            Booking.payment_status == "pending"
        )
        .all())
    return results


def get_coming_bookings(db: Session):
    return db.query(Booking).filter(Booking.booking_date > date.today(), Booking.deleted == False).all()

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return {"message": "Booking deleted"}

def mark_booking_as_paid(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.payment_status = "paid"
    booking.in_pool = True
    _marking_payment_row_of_booking_as_paid(db,booking_id)
    _updating_swimming_minutes_for_booking(db,booking,booking_id)
    db.commit()
    db.refresh(booking)
    return booking

def mark_as_out_of_pool(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.in_pool = False
    db.commit()
    db.refresh(booking)
    return booking

def cancel_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.deleted = True

    # Fetch corresponding payment
    payment = db.query(Payment).filter(Payment.booking_id == booking_id, Payment.is_deleted == False).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Associated payment not found")

    # Update payment fields
    payment.is_deleted = True
    payment.payment_date = datetime.now()  # override in case payment was generated earlier

    # Hard-delete all group members related to this booking
    group_members = db.query(GroupMember).filter(GroupMember.booking_id == booking_id).all()
    for member in group_members:
        db.delete(member)
    
    db.commit()
    db.refresh(booking)
    db.refresh(payment)
    return booking

def get_revenue_for_date(db: Session, target_date: date):
    bookings = db.query(Booking).filter(
        Booking.booking_date == target_date,
        Booking.deleted == False,
        Booking.payment_status == "paid"
    ).all()

    swimming_revenue = sum(booking.total_amount for booking in bookings)

    rental_revenue = 0
    for booking in bookings:
        for member in booking.group_members:
            rental_revenue += sum([
                member.swimwear_cost or 0,
                member.tube_cost or 0,
                member.cap_cost or 0,
                member.goggles_cost or 0,
            ])

    return {
        "swimming_revenue": swimming_revenue ,
        "rental_revenue": rental_revenue,
        "total_revenue": swimming_revenue+ rental_revenue
    }