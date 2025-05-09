<<<<<<< HEAD
from sqlalchemy.orm import Session
from models import Notice
from schemas.notices import NoticeCreate, NoticeOut
from datetime import datetime

def create_notice(db: Session, notice: NoticeCreate):
    db_notice = Notice(**notice.model_dump())
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice

def get_notices(db: Session):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

def delete_notice(db: Session, notice_id: int):
    db_notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if db_notice:
        db.delete(db_notice)
        db.commit()
        # Return the Pydantic model for response serialization
        return NoticeOut.model_dump(db_notice)
    return None
=======
from sqlalchemy.orm import Session
from models import Notice
from schemas.notices import NoticeCreate, NoticeOut
from datetime import datetime

def create_notice(db: Session, notice: NoticeCreate):
    db_notice = Notice(**notice.model_dump())
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice

def get_notices(db: Session):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

def delete_notice(db: Session, notice_id: int):
    db_notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if db_notice:
        db.delete(db_notice)
        db.commit()
        # Return the Pydantic model for response serialization
        return NoticeOut.model_dump(db_notice)
    return None
>>>>>>> origin/main
