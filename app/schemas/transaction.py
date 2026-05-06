from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    type: str
    amount: float
    note: str

class TransactionOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    type: str
    amount: float
    note: str

    class Config:
        from_attributes = True