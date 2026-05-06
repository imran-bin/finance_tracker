from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut

router = APIRouter()

@router.post("/", response_model=TransactionOut)
def create_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    new_tx = Transaction(**tx.dict())
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx


@router.get("/", response_model=list[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()