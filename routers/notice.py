from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notices import NoticeCreate, NoticeOut
from crud.notice import create_notice, get_notices ,delete_notice
from database import get_db
from models import Notice

router = APIRouter(prefix="/notices", tags=["Notices"])

# API to create a new notice
@router.post("/", response_model=NoticeOut)
def create_new_notice(notice: NoticeCreate, db: Session = Depends(get_db)):
    return create_notice(db, notice)

# API to get all notices
@router.get("/", response_model=list[NoticeOut])
def get_all_notices(db: Session = Depends(get_db)):
    return get_notices(db)

@router.delete("/{notice_id}", response_model=NoticeOut)
def delete_notice_route(notice_id: int, db: Session = Depends(get_db)):
    db_notice = delete_notice(db, notice_id)
    
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    return db_notice
