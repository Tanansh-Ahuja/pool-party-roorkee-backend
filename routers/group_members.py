<<<<<<< HEAD
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.group_members import GroupMemberCreate, GroupMemberUpdate, GroupMemberOut, GroupWithMembers
from crud import group_members as crud

router = APIRouter(prefix="/group-members", tags=["Group Members"])

@router.post("/", response_model=GroupMemberOut)
def add_group_member(member: GroupMemberCreate, db: Session = Depends(get_db)):
    return crud.create_group_member(db, member)

@router.get("/all-groups", response_model=List[GroupWithMembers])
def get_all_groups(db: Session = Depends(get_db)):
    print("Router: All groups")
    return crud.get_all_groups_with_members(db)

@router.get("/{group_id}", response_model=list[GroupMemberOut])
def get_group_by_id(group_id: str, db: Session = Depends(get_db)):
    print("Router Get group by id")
    return crud.get_group_members_by_group_id(db, group_id)

@router.get("/{group_id}/{member_id}", response_model=GroupMemberOut)
def get_one_member(group_id: str, member_id: int, db: Session = Depends(get_db)):
    member = crud.get_group_member(db, group_id, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Group member not found")
    return member

@router.put("/{group_id}/{member_id}", response_model=GroupMemberOut)
def update_member(group_id: str, member_id: int, update: GroupMemberUpdate, db: Session = Depends(get_db)):
    return crud.update_group_member(db, group_id, member_id, update)

@router.delete("/{group_id}/{member_id}")
def delete_member(group_id: str, member_id: int, db: Session = Depends(get_db)):
    success = crud.delete_group_member(db, group_id, member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group member not found")
    return {"message": "Member deleted"}


=======
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.group_members import GroupMemberCreate, GroupMemberUpdate, GroupMemberOut, GroupWithMembers
from crud import group_members as crud

router = APIRouter(prefix="/group-members", tags=["Group Members"])

@router.post("/", response_model=GroupMemberOut)
def add_group_member(member: GroupMemberCreate, db: Session = Depends(get_db)):
    return crud.create_group_member(db, member)

@router.get("/all-groups", response_model=List[GroupWithMembers])
def get_all_groups(db: Session = Depends(get_db)):
    print("Router: All groups")
    return crud.get_all_groups_with_members(db)

@router.get("/{group_id}", response_model=list[GroupMemberOut])
def get_group_by_id(group_id: str, db: Session = Depends(get_db)):
    print("Router Get group by id")
    return crud.get_group_members_by_group_id(db, group_id)

@router.get("/{group_id}/{member_id}", response_model=GroupMemberOut)
def get_one_member(group_id: str, member_id: int, db: Session = Depends(get_db)):
    member = crud.get_group_member(db, group_id, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Group member not found")
    return member

@router.put("/{group_id}/{member_id}", response_model=GroupMemberOut)
def update_member(group_id: str, member_id: int, update: GroupMemberUpdate, db: Session = Depends(get_db)):
    return crud.update_group_member(db, group_id, member_id, update)

@router.delete("/{group_id}/{member_id}")
def delete_member(group_id: str, member_id: int, db: Session = Depends(get_db)):
    success = crud.delete_group_member(db, group_id, member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group member not found")
    return {"message": "Member deleted"}


>>>>>>> origin/main
