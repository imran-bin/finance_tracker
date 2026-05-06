from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/")
def add_transaction(
    data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tx = models.Transaction(
        amount=data.amount,
        type=data.type,
        category=data.category,
        user_id=user.id
    )
    db.add(tx)
    db.commit()
    return {"msg": "Transaction added"}

@router.get("/")
def get_transactions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.Transaction).filter_by(user_id=user.id).all()