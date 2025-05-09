<<<<<<< HEAD
from collections import defaultdict
from typing import List
from sqlalchemy.orm import Session
from models import GroupMember
from schemas.group_members import GroupMemberCreate, GroupMemberUpdate, GroupMemberOut
from schemas.bookings import BookingCreate


def create_group_members(db: Session , members_data: List[GroupMemberCreate],new_booking: BookingCreate,amount_per_person: int):
    member_id_number = 0
    # Add all group members
    for member in members_data:
        member_id_number+=1
        swimwear_amount = 0
        tube_amount = 0
        cap_amount = 0
        goggles_amount = 0

        if member.needs_swimwear:
            if member.swimwear_type == "shorts":
                swimwear_amount += 20
            elif member.swimwear_type == "shorts+tshirt":
                swimwear_amount += 40
            elif member.swimwear_type == "female-set":
                swimwear_amount += 50

        if member.needs_tube:
            tube_amount += 30
        if member.needs_cap:
            cap_amount += 20
        if member.needs_goggles:
            goggles_amount += 20

        group_member = GroupMember(
            member_id = member_id_number,
            booking_id = new_booking.booking_id,
            customer_id = member.customer_id,
            full_name = member.full_name,
            age = member.age,
            gender = member.gender, 
            swimwear_type = member.swimwear_type,
            needs_swimwear = member.needs_swimwear,
            swimwear_cost = swimwear_amount,

            needs_tube = member.needs_tube,
            tube_cost = tube_amount,

            needs_cap = member.needs_cap,
            cap_cost = cap_amount,

            needs_goggles = member.needs_goggles,
            goggles_cost = goggles_amount
        )
        

        db.add(group_member)
        db.commit()
        db.refresh(group_member)

def create_group_member(db: Session, member: GroupMemberCreate):
    db_member = GroupMember(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_group_members_by_group_id(db: Session, group_id: str):
    print("Get group member by group id")
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

def get_group_member(db: Session, group_id: str, member_id: int):
    return db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_id == member_id
    ).first()

def update_group_member(db: Session, group_id: str, member_id: int, data: GroupMemberUpdate):
    member = get_group_member(db, group_id, member_id)
    if member:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
    return member

def delete_group_member(db: Session, group_id: str, member_id: int):
    member = get_group_member(db, group_id, member_id)
    if member:
        db.delete(member)
        db.commit()
        return True
    return False

def get_all_groups_with_members(db: Session):
    print("In Get All group with members")
    members = db.query(GroupMember).all()
    grouped = defaultdict(list)

    for member in members:
        grouped[member.group_id].append(member)

    # Prepare formatted output
    result = []
    for group_id, group_members in grouped.items():
        result.append({
            "group_id": group_id,
            "group_members": [GroupMemberOut.model_validate(m) for m in group_members]
        })

    return result

=======
from collections import defaultdict
from typing import List
from sqlalchemy.orm import Session
from models import GroupMember
from schemas.group_members import GroupMemberCreate, GroupMemberUpdate, GroupMemberOut
from schemas.bookings import BookingCreate


def create_group_members(db: Session , members_data: List[GroupMemberCreate],new_booking: BookingCreate,amount_per_person: int):
    member_id_number = 0
    # Add all group members
    for member in members_data:
        member_id_number+=1
        swimwear_amount = 0
        tube_amount = 0
        cap_amount = 0
        goggles_amount = 0

        if member.needs_swimwear:
            if member.swimwear_type == "shorts":
                swimwear_amount += 20
            elif member.swimwear_type == "shorts+tshirt":
                swimwear_amount += 40
            elif member.swimwear_type == "female-set":
                swimwear_amount += 50

        if member.needs_tube:
            tube_amount += 30
        if member.needs_cap:
            cap_amount += 20
        if member.needs_goggles:
            goggles_amount += 20

        group_member = GroupMember(
            member_id = member_id_number,
            booking_id = new_booking.booking_id,
            customer_id = member.customer_id,
            full_name = member.full_name,
            age = member.age,
            gender = member.gender, 
            swimwear_type = member.swimwear_type,
            needs_swimwear = member.needs_swimwear,
            swimwear_cost = swimwear_amount,

            needs_tube = member.needs_tube,
            tube_cost = tube_amount,

            needs_cap = member.needs_cap,
            cap_cost = cap_amount,

            needs_goggles = member.needs_goggles,
            goggles_cost = goggles_amount
        )
        

        db.add(group_member)
        db.commit()
        db.refresh(group_member)

def create_group_member(db: Session, member: GroupMemberCreate):
    db_member = GroupMember(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_group_members_by_group_id(db: Session, group_id: str):
    print("Get group member by group id")
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

def get_group_member(db: Session, group_id: str, member_id: int):
    return db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_id == member_id
    ).first()

def update_group_member(db: Session, group_id: str, member_id: int, data: GroupMemberUpdate):
    member = get_group_member(db, group_id, member_id)
    if member:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
    return member

def delete_group_member(db: Session, group_id: str, member_id: int):
    member = get_group_member(db, group_id, member_id)
    if member:
        db.delete(member)
        db.commit()
        return True
    return False

def get_all_groups_with_members(db: Session):
    print("In Get All group with members")
    members = db.query(GroupMember).all()
    grouped = defaultdict(list)

    for member in members:
        grouped[member.group_id].append(member)

    # Prepare formatted output
    result = []
    for group_id, group_members in grouped.items():
        result.append({
            "group_id": group_id,
            "group_members": [GroupMemberOut.model_validate(m) for m in group_members]
        })

    return result

>>>>>>> origin/main
