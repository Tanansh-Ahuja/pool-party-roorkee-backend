from typing import Optional
from pydantic import BaseModel
from datetime import date, time

class BlockedDateBase(BaseModel):
    blocked_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    reason: Optional[str] = None


class BlockedDateCreate(BlockedDateBase):
    pass

class BlockedDateUpdate(BlockedDateBase):
    pass

class BlockedDateOut(BlockedDateBase):
    blocked_id: int

    class Config:
        from_attributes = True


