from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(status_code=401)

        return payload["user_id"]

    except:
        raise HTTPException(status_code=401, detail="Unauthorized")