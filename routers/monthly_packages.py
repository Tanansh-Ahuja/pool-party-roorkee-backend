<<<<<<< HEAD
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import monthly_packages
from schemas.monthly_packages import MonthlyPackageCreate, MonthlyPackageUpdate, MonthlyPackageOut, StatusRefreshResult
from database import get_db

router = APIRouter(prefix="/monthly-packages", tags=["monthly-packages"])

@router.post("/", response_model=MonthlyPackageOut)
def create_monthly_package(package: MonthlyPackageCreate, db: Session = Depends(get_db)):
    return monthly_packages.create_monthly_package(db=db, package=package)

@router.get("/", response_model=list[MonthlyPackageOut])
def get_monthly_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return monthly_packages.get_monthly_packages(db=db, skip=skip, limit=limit)

@router.post("/refresh-status", response_model=StatusRefreshResult)
def refresh_statuses(db: Session = Depends(get_db)):
    updated = monthly_packages.refresh_package_statuses(db)
    return StatusRefreshResult(
        updated_count=updated,
        message=f"{updated} package(s) marked as expired."
    )

@router.get("/{package_id}", response_model=MonthlyPackageOut)
def get_monthly_package(package_id: int, db: Session = Depends(get_db)):
    return monthly_packages.get_monthly_package_by_id(db=db, package_id=package_id)

@router.put("/{package_id}", response_model=MonthlyPackageOut)
def update_monthly_package(package_id: int, package: MonthlyPackageUpdate, db: Session = Depends(get_db)):
    return monthly_packages.update_monthly_package(db=db, package_id=package_id, package=package)


=======
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import monthly_packages
from schemas.monthly_packages import MonthlyPackageCreate, MonthlyPackageUpdate, MonthlyPackageOut, StatusRefreshResult
from database import get_db

router = APIRouter(prefix="/monthly-packages", tags=["monthly-packages"])

@router.post("/", response_model=MonthlyPackageOut)
def create_monthly_package(package: MonthlyPackageCreate, db: Session = Depends(get_db)):
    return monthly_packages.create_monthly_package(db=db, package=package)

@router.get("/", response_model=list[MonthlyPackageOut])
def get_monthly_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return monthly_packages.get_monthly_packages(db=db, skip=skip, limit=limit)

@router.post("/refresh-status", response_model=StatusRefreshResult)
def refresh_statuses(db: Session = Depends(get_db)):
    updated = monthly_packages.refresh_package_statuses(db)
    return StatusRefreshResult(
        updated_count=updated,
        message=f"{updated} package(s) marked as expired."
    )

@router.get("/{package_id}", response_model=MonthlyPackageOut)
def get_monthly_package(package_id: int, db: Session = Depends(get_db)):
    return monthly_packages.get_monthly_package_by_id(db=db, package_id=package_id)

@router.put("/{package_id}", response_model=MonthlyPackageOut)
def update_monthly_package(package_id: int, package: MonthlyPackageUpdate, db: Session = Depends(get_db)):
    return monthly_packages.update_monthly_package(db=db, package_id=package_id, package=package)


>>>>>>> origin/main
