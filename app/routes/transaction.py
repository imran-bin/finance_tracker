from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import TransactionCreate

router = APIRouter()

@router.post("/")
def add_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    # Verify category exists for this user, or use a default one
    category = db.query(Category).filter(
        Category.id == tx.category_id, 
        Category.user_id == tx.user_id
    ).first()

    # If category doesn't exist, try to find ANY category for this user
    if not category:
        category = db.query(Category).filter(Category.user_id == tx.user_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="User has no categories. Please register again or add a category.")
        tx.category_id = category.id

    t = Transaction(
        user_id=tx.user_id,
        category_id=tx.category_id,
        type=tx.type,
        amount=tx.amount,
        note=tx.note,
        date=tx.date
    )
    
    try:
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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