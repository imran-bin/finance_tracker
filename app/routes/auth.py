from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
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
        {"name": "remittance", "type": "income"},
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
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
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

    # Set cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='none', secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite='none', secure=True)

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
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)

    # Set cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='none', secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite='none', secure=True)

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

@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    # 1. Try to get token from Cookie
    token = request.cookies.get("access_token")
    
    # 2. If no cookie, try to get token from Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from app.core.security import verify_token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email
    }

@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    from app.core.security import verify_token
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    new_access_token = create_access_token(user_id)
    
    # Update cookie
    response.set_cookie(key="access_token", value=new_access_token, httponly=True, samesite='none', secure=True)
    
    return {"access_token": new_access_token}
