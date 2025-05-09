from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, date, time

class GroupMemberBase(BaseModel):
    member_id: int
    booking_id: int
    full_name: str
    customer_id: Optional[int] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    needs_swimwear: bool = False
    swimwear_type: Optional[str] = None
    swimwear_cost: Decimal = 0.00
    needs_tube: bool = False
    tube_cost: Decimal = 0.00
    needs_cap: bool = False
    cap_cost: Decimal = 0.00
    needs_goggles: bool = False
    goggles_cost: Decimal = 0.00
    special_notes: Optional[str] = None

class GroupMemberCreate(BaseModel):
    customer_id:Optional[int]=None
    full_name: str
    age: int
    gender: str
    needs_swimwear: bool = False
    swimwear_type: Optional[str] = None  # shorts, shorts+tshirt, female-set
    needs_tube: bool = False
    needs_cap: bool = False
    needs_goggles: bool = False
    booking_time: datetime
    booking_date: date
    slot_start: time
    slot_end: time

# Model for what we save in DB (DB Model) - extra fields like IDs
class GroupMemberDB(GroupMemberCreate):
    member_id: int
    booking_id: int
    booking_time: datetime
    special_notes: Optional[str] = None

class GroupMemberUpdate(BaseModel):
    age: Optional[int]
    gender: Optional[str]
    needs_swimwear: Optional[bool]
    swimwear_type: Optional[str]
    swimwear_cost: Optional[Decimal]
    needs_tube: Optional[bool]
    tube_cost: Optional[Decimal]
    needs_cap: Optional[bool]
    cap_cost: Optional[Decimal]
    needs_goggles: Optional[bool]
    goggles_cost: Optional[Decimal]
    special_notes: Optional[str]

class GroupMemberOut(GroupMemberBase):
    member_id: int
    booking_id: int
    full_name: str
    customer_id: Optional[int]
    age: Optional[int]
    gender: Optional[str]
    needs_swimwear: Optional[bool]
    swimwear_type: Optional[str]
    swimwear_cost: Optional[Decimal]
    needs_tube: Optional[bool]
    tube_cost: Optional[Decimal]
    needs_cap: Optional[bool]
    cap_cost: Optional[Decimal]
    needs_goggles: Optional[bool]
    goggles_cost: Optional[Decimal]
    special_notes: Optional[str]
    class Config:
        from_attributes = True


class GroupWithMembers(BaseModel):
    booking_id: int
    group_members: List[GroupMemberOut]
