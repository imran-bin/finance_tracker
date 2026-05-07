from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate

router = APIRouter()

@router.post("/")
def create_category(cat: CategoryCreate, db: Session = Depends(get_db)):
    c = Category(**cat.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/{user_id}")
def get_categories(user_id: int, db: Session = Depends(get_db)):
    # Also return some default categories if user has none
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    if not categories:
        # Default categories logic could go here or on frontend
        pass
    return categories