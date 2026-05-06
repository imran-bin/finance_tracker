from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)  # income / expense
    user_id = Column(Integer, ForeignKey("users.id"))