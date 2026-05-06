from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    type: str
    amount: float
    note: str
    date: datetime | None = None