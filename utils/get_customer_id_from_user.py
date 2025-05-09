from models import Customer
from fastapi import HTTPException

def get_customer_id_from_user_id(db, user_id: int) -> int:
    customer = db.query(Customer).filter(Customer.user_id == user_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer profile not found for this user.")
    return customer.customer_id