from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Attendance
from database import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter()


class AttendanceCreate(BaseModel):
    employee_id: int
    check_in: str
    check_out: str


class AttendanceOut(AttendanceCreate):
    id: int


@router.post("/", response_model=AttendanceOut)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


@router.get("/", response_model=List[AttendanceOut])
def read_attendance(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).offset(skip).limit(limit).all()
    return attendance


@router.get("/{attendance_id}", response_model=AttendanceOut)
def read_attendance_record(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(attendance_id: int, attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    for key, value in attendance.dict().items():
        setattr(db_attendance, key, value)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(db_attendance)
    db.commit()
    return {"detail": "Attendance record deleted"}
