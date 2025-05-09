from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import settings as crud_settings

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/booking-enabled")
def check_booking_status(db: Session = Depends(get_db)):
    return {"booking_enabled": crud_settings.is_booking_enabled(db)}

@router.put("/booking-enabled/{enabled}")
def toggle_booking_status(enabled: bool, db: Session = Depends(get_db)):
    new_status = crud_settings.set_booking_enabled(db, enabled)
    return {"booking_enabled": new_status}
