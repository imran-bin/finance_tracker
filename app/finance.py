from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt
import os

from db import get_db
from models import Transaction
from schemas import TransactionCreate

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")


def get_user_id(token: str):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return data["user_id"]


@router.post("/add")
def add(tx: TransactionCreate, token: str, db: Session = Depends(get_db)):
    user_id = get_user_id(token)

    new_tx = Transaction(
        amount=tx.amount,
        type=tx.type,
        user_id=user_id
    )

    db.add(new_tx)
    db.commit()

    return {"msg": "added"}


@router.get("/all")
def all_transactions(token: str, db: Session = Depends(get_db)):
    user_id = get_user_id(token)

    data = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return data