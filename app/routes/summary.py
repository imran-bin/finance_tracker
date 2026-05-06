from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.transaction import Transaction

router = APIRouter()

@router.get("/monthly/{user_id}")
def monthly_summary(user_id: int, db: Session = Depends(get_db)):

    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income"
    ).scalar() or 0

    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense"
    ).scalar() or 0

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }