from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class TransactionCreate(BaseModel):
    amount: float
    type: str