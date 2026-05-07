from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.category import Category
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password

router = APIRouter()

def seed_categories(user_id: int, db: Session):
    defaults = [
        {"name": "salary", "type": "income"},
        {"name": "freelance", "type": "income"},
        {"name": "food", "type": "expense"},
        {"name": "transport", "type": "expense"},
        {"name": "shopping", "type": "expense"},
        {"name": "health", "type": "expense"},
    ]
    for item in defaults:
        cat = Category(name=item["name"], type=item["type"], user_id=user_id)
        db.add(cat)
    db.commit()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Seed default categories for the new user
    seed_categories(new_user.id, db)

    return {
        "message": "User created successfully with default categories",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }