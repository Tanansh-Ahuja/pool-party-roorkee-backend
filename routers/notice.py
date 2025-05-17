from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notices import NoticeCreate, NoticeOut, NoticeUpdate
from crud.notice import create_one_notice, get_notices ,delete_notice_by_id, update_one_notice
from database import get_db
from models import Notice

router = APIRouter(prefix="/notices", tags=["Notices"])

# API to create a new notice
@router.post("/", response_model=NoticeOut)
def create_notice(notice: NoticeCreate, db: Session = Depends(get_db)):
    return create_one_notice(db, notice)

# API to get all notices
@router.get("/", response_model=list[NoticeOut])
def get_all_notices(db: Session = Depends(get_db)):
    return get_notices(db)

@router.put("/{notice_id}")
def update_notice(notice_id: int, notice_update: NoticeUpdate, db: Session = Depends(get_db)):
    return update_one_notice(notice_id,notice_update,db)
    

@router.delete("/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    return delete_notice_by_id(notice_id, db)
