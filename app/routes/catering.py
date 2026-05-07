from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.models.catering import CateringLog
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class MealSaveRequest(BaseModel):
    user_id: int
    meal_date: date
    lunch: bool
    dinner: bool
    extra: int
    lunch_food: Optional[str] = ""
    dinner_food: Optional[str] = ""
    extra_food: Optional[str] = ""

@router.get("/{user_id}")
def get_catering_logs(user_id: int, db: Session = Depends(get_db)):
    return db.query(CateringLog).filter(CateringLog.user_id == user_id).order_by(CateringLog.date.desc()).all()

@router.post("/save")
def save_meal_log(data: MealSaveRequest, db: Session = Depends(get_db)):
    log = db.query(CateringLog).filter(CateringLog.user_id == data.user_id, CateringLog.date == data.meal_date).first()
    if not log:
        log = CateringLog(user_id=data.user_id, date=data.meal_date)
        db.add(log)
    
    log.lunch = data.lunch
    log.dinner = data.dinner
    log.extra = data.extra
    
    log.lunch_food = data.lunch_food
    log.dinner_food = data.dinner_food
    log.extra_food = data.extra_food
    
    db.commit()
    db.refresh(log)
    return log

@router.get("/{user_id}/summary")
def get_catering_summary(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(CateringLog).filter(CateringLog.user_id == user_id).all()
    total_meals = sum([ 
        (1 if log.lunch else 0) + (1 if log.dinner else 0) + (log.extra if log.extra else 0) 
        for log in logs 
    ])
    total_bill = total_meals * 80
    return {"total_meals": total_meals, "total_bill": total_bill}
