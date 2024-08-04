from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import PerformanceReview
from database import get_db
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()


class PerformanceReviewCreate(BaseModel):
    employee_id: int
    review_date: date
    reviewer_id: int
    comments: str


class PerformanceReviewOut(PerformanceReviewCreate):
    id: int


@router.post("/", response_model=PerformanceReviewOut)
def create_performance_review(review: PerformanceReviewCreate, db: Session = Depends(get_db)):
    db_review = PerformanceReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/", response_model=List[PerformanceReviewOut])
def read_performance_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = db.query(PerformanceReview).offset(skip).limit(limit).all()
    return reviews


@router.get("/{review_id}", response_model=PerformanceReviewOut)
def read_performance_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Performance review not found")
    return review


@router.put("/{review_id}", response_model=PerformanceReviewOut)
def update_performance_review(review_id: int, review: PerformanceReviewCreate, db: Session = Depends(get_db)):
    db_review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Performance review not found")
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/{review_id}")
def delete_performance_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Performance review not found")
    db.delete(db_review)
    db.commit()
    return {"detail": "Performance review deleted"}
