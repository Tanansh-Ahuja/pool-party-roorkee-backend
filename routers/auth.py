from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Customer
from schemas.user import UserCreate, UserLogin, UserOut
from database import get_db
from utils.auth import hash_password, verify_password
from utils.jwt_token import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Email uniqueness check (if provided)
    if user.email and db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Username uniqueness check (if provided)
    if user.username and db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Mobile number is required — always check
    if db.query(Customer).filter(Customer.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Mobile number already taken")

    hashed_pw = hash_password(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role.lower() == "customer":
        customer = Customer(
            full_name=user.full_name,
            phone_number=user.phone_number,
            gender=user.gender,
            age=user.age,
            swimming_minutes=0,
            notes=user.notes,
            user_id=new_user.user_id
        )
        db.add(customer)
        db.commit()

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = None

    # Try login by email
    if user.email:
        db_user = db.query(User).filter(User.email == user.email).first()
    
    # Try login by phone number (go through customers table)
    elif user.phone_number:
        customer = db.query(Customer).filter(Customer.phone_number == user.phone_number).first()
        if customer:
            db_user = db.query(User).filter(User.user_id == customer.user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate the JWT token
    user_data = {
        "sub": db_user.email or str(db_user.user_id),  # fallback if no email
        "id": db_user.user_id,
        "role": db_user.role
    }
    access_token = create_access_token(user_data)
    
    return access_token
