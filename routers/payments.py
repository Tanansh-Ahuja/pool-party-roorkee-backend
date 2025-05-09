<<<<<<< HEAD
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import payments
from schemas.payments import PaymentCreate, PaymentUpdate, PaymentOut
from database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payments.create_payment(db=db, payment=payment)

@router.get("/", response_model=list[PaymentOut])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return payments.get_payments(db=db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payments.get_payment_by_id(db=db, payment_id=payment_id)

@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    return payments.update_payment(db=db, payment_id=payment_id, payment=payment)
=======
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import payments
from schemas.payments import PaymentCreate, PaymentUpdate, PaymentOut
from database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payments.create_payment(db=db, payment=payment)

@router.get("/", response_model=list[PaymentOut])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return payments.get_payments(db=db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payments.get_payment_by_id(db=db, payment_id=payment_id)

@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    return payments.update_payment(db=db, payment_id=payment_id, payment=payment)
>>>>>>> origin/main
