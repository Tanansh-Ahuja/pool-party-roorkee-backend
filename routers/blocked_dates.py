from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import blocked_dates
from schemas.blocked_dates import BlockedDateCreate, BlockedDateUpdate, BlockedDateOut
from database import get_db

router = APIRouter( prefix="/blocked-dates", tags=["blocked-dates"])

@router.post("/", response_model=BlockedDateOut)
def create_blocked_date(blocked_date: BlockedDateCreate, db: Session = Depends(get_db)):
    return blocked_dates.create_blocked_date(db=db, blocked_date=blocked_date)

@router.get("/", response_model=list[BlockedDateOut])
def get_blocked_dates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return blocked_dates.get_blocked_dates(db=db, skip=skip, limit=limit)

@router.get("/{blocked_date_id}", response_model=BlockedDateOut)
def get_blocked_date(blocked_date_id: int, db: Session = Depends(get_db)):
    return blocked_dates.get_blocked_date_by_id(db=db, blocked_date_id=blocked_date_id)

@router.put("/{blocked_date_id}", response_model=BlockedDateOut)
def update_blocked_date(blocked_date_id: int, blocked_date: BlockedDateUpdate, db: Session = Depends(get_db)):
    return blocked_dates.update_blocked_date(db=db, blocked_date_id=blocked_date_id, blocked_date=blocked_date)

@router.delete("/{blocked_date_id}", status_code=204)
def delete_blocked_date(blocked_date_id: int, db: Session = Depends(get_db)):
    success = blocked_dates.delete_blocked_date(db, blocked_date_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blocked date not found")
    return
