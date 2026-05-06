from fastapi import APIRouter
from db.database import SessionLocal
from db.models import User
from core.security import create_access_token, create_refresh_token
from passlib.hash import bcrypt
from jose import jwt
import os

router = APIRouter()


@router.post("/register")
def register(username: str, password: str):
    db = SessionLocal()

    user = User(
        username=username,
        password=bcrypt.hash(password)
    )

    db.add(user)
    db.commit()

    return {"msg": "user created"}


@router.post("/login")
def login(username: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(password, user.password):
        return {"error": "invalid"}

    access = create_access_token({"user_id": user.id})
    refresh = create_refresh_token({"user_id": user.id})

    return {"access": access, "refresh": refresh}


@router.post("/refresh")
def refresh(token: str):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

    new_access = create_access_token({"user_id": payload["user_id"]})

    return {"access": new_access}