from fastapi import Depends, HTTPException
from scipy import stats
from sqlalchemy.orm import Session
from models import Customer, User
from schemas.customers import CustomerCreate, CustomerUserUpdate
from utils.auth import get_current_user

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_me(db: Session, current_user: User = Depends(get_current_user)):
    # assuming user.email is stored in both user and customer
    customer = db.query(Customer).filter(Customer.user_id == current_user.user_id).first()
    if not customer:
        raise HTTPException(
            status_code=stats.HTTP_404_NOT_FOUND,
            detail="Customer profile not found."
        )
    return {
        "customer_id": customer.customer_id,
        "full_name": customer.full_name,
        "phone_number": customer.phone_number,
        "gender": customer.gender,
        "age": customer.age,
        "swimming_minutes": customer.swimming_minutes,
        "registered_at":customer.registered_at,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

def get_customer_by_customer_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def get_all_customers(db: Session):
    return db.query(Customer).all()

def update_customer(db: Session, customer_id: int, updated_data: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer:
        for key, value in updated_data.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return {"message": "Customer deleted"}

def update_customer_and_user_by_user_id(db: Session, user_id: int, updated_data: CustomerUserUpdate):
    customer = db.query(Customer).filter(Customer.user_id == user_id).first()
    user = db.query(User).filter(User.user_id == user_id).first()

    if not customer or not user:
        return None

    update_dict = updated_data.model_dump(exclude_unset=True)
    
    # Separate and update user fields
    user_fields = ["username", "email"]
    for field in user_fields:
        if field in update_dict:
            setattr(user, field, update_dict[field])

    # Update customer fields
    for field in update_dict:
        if field not in user_fields:
            setattr(customer, field, update_dict[field])

    db.commit()
    db.refresh(customer)
    return customer