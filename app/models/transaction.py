from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    type = Column(String)  # income / expense
    amount = Column(Float)
    note = Column(String)
    date = Column(DateTime, default=datetime.utcnow)