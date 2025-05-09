<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel
from datetime import date

class MonthlyPackageBase(BaseModel):
    customer_id: int
    start_date: date
    end_date: date
    total_price: float
    discount_percentage: Optional[int] = 0
    package_status: str = 'active'

class MonthlyPackageCreate(MonthlyPackageBase):
    pass

class MonthlyPackageUpdate(BaseModel):
    end_date: Optional[date]
    total_price: Optional[float]
    discount_percentage: Optional[int]
    package_status: Optional[str]

class MonthlyPackageOut(MonthlyPackageBase):
    class Config:
        from_attributes = True

class StatusRefreshResult(BaseModel):
    updated_count: int
    message: str
=======
from typing import Optional
from pydantic import BaseModel
from datetime import date

class MonthlyPackageBase(BaseModel):
    customer_id: int
    start_date: date
    end_date: date
    total_price: float
    discount_percentage: Optional[int] = 0
    package_status: str = 'active'

class MonthlyPackageCreate(MonthlyPackageBase):
    pass

class MonthlyPackageUpdate(BaseModel):
    end_date: Optional[date]
    total_price: Optional[float]
    discount_percentage: Optional[int]
    package_status: Optional[str]

class MonthlyPackageOut(MonthlyPackageBase):
    class Config:
        from_attributes = True

class StatusRefreshResult(BaseModel):
    updated_count: int
    message: str
>>>>>>> origin/main
