from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
import crud.earnings as earnings_crud

router = APIRouter(prefix="/earnings", tags=["Earnings"])

@router.get("/today")
def get_todays_earnings(db: Session = Depends(get_db)):
    return earnings_crud.get_total_earnings_for_date(db, date.today())

@router.get("/earning_for_date")
def get_earnings_for_specific_date(
    target_date: date = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    return earnings_crud.get_total_earnings_for_date(db, target_date)
