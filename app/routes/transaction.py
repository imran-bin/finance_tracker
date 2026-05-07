from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

router = APIRouter()

@router.post("/")
def add_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    t = Transaction(**tx.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get("/{user_id}")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.date.desc()).all()

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(t)
    db.commit()
    return {"message": "Transaction deleted"}