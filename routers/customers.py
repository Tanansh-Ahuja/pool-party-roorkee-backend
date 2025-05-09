<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.customers import CustomerCreate, CustomerOut, CustomerUpdate, CustomerProfileOut
from crud.customers import update_customer_by_user_id, create_customer, get_customer_by_customer_id, get_all_customers, update_customer, delete_customer, get_me
from utils.auth import get_current_user
from models import User

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerOut)
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@router.get("/", response_model=list[CustomerOut])
def read_all_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.get("/me", response_model=CustomerProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_me(db,current_user)
    

@router.put("/UpdateMe", response_model=CustomerOut)
def update_my_customer_profile(
    updated_info: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_customer = update_customer_by_user_id(db, current_user.user_id, updated_info)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.get("/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_customer_by_customer_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer_route(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    return update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
def delete_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, customer_id)
=======
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.customers import CustomerCreate, CustomerOut, CustomerUpdate, CustomerProfileOut
from crud.customers import update_customer_by_user_id, create_customer, get_customer_by_customer_id, get_all_customers, update_customer, delete_customer, get_me
from utils.auth import get_current_user
from models import User

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerOut)
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@router.get("/", response_model=list[CustomerOut])
def read_all_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.get("/me", response_model=CustomerProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_me(db,current_user)
    

@router.put("/UpdateMe", response_model=CustomerOut)
def update_my_customer_profile(
    updated_info: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_customer = update_customer_by_user_id(db, current_user.user_id, updated_info)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.get("/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_customer_by_customer_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer_route(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    return update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
def delete_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, customer_id)
>>>>>>> origin/main
