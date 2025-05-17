from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import Notice
from schemas.notices import NoticeCreate, NoticeOut, NoticeUpdate
from datetime import datetime
from database import get_db

def create_one_notice(db: Session, notice: NoticeCreate):
    new_notice = Notice(title=notice.title, content=notice.content)
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

def get_notices(db: Session):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

def update_one_notice(notice_id: int, notice_update: NoticeUpdate, db: Session = Depends(get_db)):
    db_notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if notice_update.title is not None:
        db_notice.title = notice_update.title
    if notice_update.content is not None:
        db_notice.content = notice_update.content

    db.commit()
    db.refresh(db_notice)
    return {"message": "Notice updated successfully", "notice": {
        "id": db_notice.id,
        "heading": db_notice.title,
        "content": db_notice.content
    }}

def delete_notice_by_id(notice_id: int, db: Session):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    db.delete(notice)
    db.commit()
    return {"detail": f"Notice {notice_id} deleted successfully"}
        
