from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Leave
from database import get_db
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()


class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str


class LeaveOut(LeaveCreate):
    id: int


@router.post("/", response_model=LeaveOut)
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    db_leave = Leave(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


@router.get("/", response_model=List[LeaveOut])
def read_leaves(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leaves = db.query(Leave).offset(skip).limit(limit).all()
    return leaves


@router.get("/{leave_id}", response_model=LeaveOut)
def read_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave


@router.put("/{leave_id}", response_model=LeaveOut)
def update_leave(leave_id: int, leave: LeaveCreate, db: Session = Depends(get_db)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    for key, value in leave.dict().items():
        setattr(db_leave, key, value)
    db.commit()
    db.refresh(db_leave)
    return db_leave


@router.delete("/{leave_id}")
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    db.delete(db_leave)
    db.commit()
    return {"detail": "Leave deleted"}
