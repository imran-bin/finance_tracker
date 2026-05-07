from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category

router = APIRouter()

@router.get("/dashboard/{user_id}")
def dashboard_summary(user_id: int, db: Session = Depends(get_db)):
    # Stats
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income"
    ).scalar() or 0

    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense"
    ).scalar() or 0

    # Recent Transactions
    recent_transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).limit(5).all()

    # Category Breakdown (Expenses only)
    category_data = db.query(
        Category.name,
        func.sum(Transaction.amount).label("value")
    ).join(Transaction, Category.id == Transaction.category_id).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense"
    ).group_by(Category.name).all()

    # Format category data for frontend
    formatted_categories = [
        {"name": c.name, "value": float(c.value)} for c in category_data
    ]

    return {
        "stats": {
            "income": income,
            "expense": expense,
            "balance": income - expense
        },
        "recent_transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.type,
                "note": t.note,
                "date": t.date.isoformat(),
                "category_id": t.category_id
            } for t in recent_transactions
        ],
        "categories": formatted_categories
    }

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