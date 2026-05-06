from fastapi import APIRouter, Depends
from db.database import SessionLocal
from db.models import Transaction
from middleware.auth import get_current_user

router = APIRouter()


@router.post("/add")
def add(amount: float, type: str, user_id=Depends(get_current_user)):
    db = SessionLocal()

    tx = Transaction(user_id=user_id, amount=amount, type=type)

    db.add(tx)
    db.commit()

    return {"msg": "saved"}


@router.get("/balance")
def balance(user_id=Depends(get_current_user)):
    db = SessionLocal()

    txs = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    income = sum(t.amount for t in txs if t.type == "income")
    expense = sum(t.amount for t in txs if t.type == "expense")

    return {"balance": income - expense}