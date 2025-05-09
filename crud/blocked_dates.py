<<<<<<< HEAD
from sqlalchemy.orm import Session
from models import BlockedDate
from schemas.blocked_dates import BlockedDateCreate, BlockedDateUpdate

def create_blocked_date(db: Session, blocked_date: BlockedDateCreate):
    db_blocked_date = BlockedDate(**blocked_date.model_dump())
    db.add(db_blocked_date)
    db.commit()
    db.refresh(db_blocked_date)
    return db_blocked_date

def get_blocked_dates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlockedDate).offset(skip).limit(limit).all()

def get_blocked_date_by_id(db: Session, blocked_date_id: int):
    return db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()

def update_blocked_date(db: Session, blocked_date_id: int, blocked_date: BlockedDateUpdate):
    db_blocked_date = db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()
    if db_blocked_date:
        for key, value in blocked_date.model_dump(exclude_unset=True).items():
            setattr(db_blocked_date, key, value)
        db.commit()
        db.refresh(db_blocked_date)
        return db_blocked_date
    return None

def delete_blocked_date(db: Session, blocked_date_id: int):
    db_block = db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()
    if db_block:
        db.delete(db_block)
        db.commit()
        return True
    return False
=======
from sqlalchemy.orm import Session
from models import BlockedDate
from schemas.blocked_dates import BlockedDateCreate, BlockedDateUpdate

def create_blocked_date(db: Session, blocked_date: BlockedDateCreate):
    db_blocked_date = BlockedDate(**blocked_date.model_dump())
    db.add(db_blocked_date)
    db.commit()
    db.refresh(db_blocked_date)
    return db_blocked_date

def get_blocked_dates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlockedDate).offset(skip).limit(limit).all()

def get_blocked_date_by_id(db: Session, blocked_date_id: int):
    return db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()

def update_blocked_date(db: Session, blocked_date_id: int, blocked_date: BlockedDateUpdate):
    db_blocked_date = db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()
    if db_blocked_date:
        for key, value in blocked_date.model_dump(exclude_unset=True).items():
            setattr(db_blocked_date, key, value)
        db.commit()
        db.refresh(db_blocked_date)
        return db_blocked_date
    return None

def delete_blocked_date(db: Session, blocked_date_id: int):
    db_block = db.query(BlockedDate).filter(BlockedDate.blocked_id == blocked_date_id).first()
    if db_block:
        db.delete(db_block)
        db.commit()
        return True
    return False
>>>>>>> origin/main
