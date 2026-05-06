from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()