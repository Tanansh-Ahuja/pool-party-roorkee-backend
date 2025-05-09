from pydantic import BaseModel
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoticeCreate(NoticeBase):
    pass

class NoticeOut(NoticeBase):
    id: int
