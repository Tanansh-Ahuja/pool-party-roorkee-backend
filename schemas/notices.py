from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NoticeCreate(BaseModel):
    title: str
    content: str

class NoticeBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoticeOut(NoticeBase):
    id: int

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None