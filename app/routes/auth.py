from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.category import Category
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

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
    seed_categories(new_user.id, db)

    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    return {
        "message": "User created successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # Simple refresh logic
    from app.core.security import verify_token
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    new_access_token = create_access_token(user_id)
    return {"access_token": new_access_token}