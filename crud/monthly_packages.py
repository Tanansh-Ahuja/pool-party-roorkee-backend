<<<<<<< HEAD
from datetime import date
from sqlalchemy.orm import Session
from models import MonthlyPackage
from schemas.monthly_packages import MonthlyPackageCreate, MonthlyPackageUpdate

def create_monthly_package(db: Session, package: MonthlyPackageCreate):
    db_package = MonthlyPackage(**package.dict())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def get_monthly_packages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MonthlyPackage).offset(skip).limit(limit).all()

def get_monthly_package_by_id(db: Session, package_id: int):
    return db.query(MonthlyPackage).filter(MonthlyPackage.package_id == package_id).first()

def update_monthly_package(db: Session, package_id: int, package: MonthlyPackageUpdate):
    db_package = db.query(MonthlyPackage).filter(MonthlyPackage.package_id == package_id).first()
    if db_package:
        for key, value in package.dict(exclude_unset=True).items():
            setattr(db_package, key, value)
        db.commit()
        db.refresh(db_package)
        return db_package
    return None

def refresh_package_statuses(db: Session):
    today = date.today()
    expired_packages = (
        db.query(MonthlyPackage)
        .filter(MonthlyPackage.end_date < today, MonthlyPackage.package_status == "active")
        .all()
    )

    count = 0
    for package in expired_packages:
        package.package_status = "expired"
        count += 1

    db.commit()
    return count
=======
from datetime import date
from sqlalchemy.orm import Session
from models import MonthlyPackage
from schemas.monthly_packages import MonthlyPackageCreate, MonthlyPackageUpdate

def create_monthly_package(db: Session, package: MonthlyPackageCreate):
    db_package = MonthlyPackage(**package.dict())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def get_monthly_packages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MonthlyPackage).offset(skip).limit(limit).all()

def get_monthly_package_by_id(db: Session, package_id: int):
    return db.query(MonthlyPackage).filter(MonthlyPackage.package_id == package_id).first()

def update_monthly_package(db: Session, package_id: int, package: MonthlyPackageUpdate):
    db_package = db.query(MonthlyPackage).filter(MonthlyPackage.package_id == package_id).first()
    if db_package:
        for key, value in package.dict(exclude_unset=True).items():
            setattr(db_package, key, value)
        db.commit()
        db.refresh(db_package)
        return db_package
    return None

def refresh_package_statuses(db: Session):
    today = date.today()
    expired_packages = (
        db.query(MonthlyPackage)
        .filter(MonthlyPackage.end_date < today, MonthlyPackage.package_status == "active")
        .all()
    )

    count = 0
    for package in expired_packages:
        package.package_status = "expired"
        count += 1

    db.commit()
    return count
>>>>>>> origin/main
