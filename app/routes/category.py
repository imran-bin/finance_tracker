from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()