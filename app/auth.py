from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from db import get_db
from models import User
from schemas import UserCreate
import os

router = APIRouter()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd.hash(user.password)
    new_user = User(email=user.email, password=hashed)

    db.add(new_user)
    db.commit()
    return {"msg": "user created"}


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd.verify(user.password, db_user.password):
        return {"error": "invalid credentials"}

    token = jwt.encode(
        {"user_id": db_user.id},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"access_token": token}