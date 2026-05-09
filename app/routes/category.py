from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate

router = APIRouter()

VALID_CATEGORY_TYPES = {"income", "expense"}

@router.post("/")
def create_category(cat: CategoryCreate, db: Session = Depends(get_db)):
    if cat.type not in VALID_CATEGORY_TYPES:
        raise HTTPException(status_code=400, detail="Category type must be income or expense")

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

@router.put("/{category_id}")
def update_category(category_id: int, cat: CategoryUpdate, db: Session = Depends(get_db)):
    if cat.type not in VALID_CATEGORY_TYPES:
        raise HTTPException(status_code=400, detail="Category type must be income or expense")

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == cat.user_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = cat.name
    category.type = cat.type

    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, user_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    is_used = db.query(Transaction).filter(
        Transaction.category_id == category_id,
        Transaction.user_id == user_id
    ).first()
    if is_used:
        raise HTTPException(
            status_code=400,
            detail="This category is used by transactions. Move or delete those transactions first."
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
