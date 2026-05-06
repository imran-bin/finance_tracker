from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str