from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, String
from app.core.database import Base

class CateringLog(Base):
    __tablename__ = "catering_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, unique=True, index=True)
    
    # Meals
    lunch = Column(Boolean, default=False)
    dinner = Column(Boolean, default=False)
    extra = Column(Integer, default=0) # Now an Integer for count
    
    # Food Names
    lunch_food = Column(String, nullable=True)
    dinner_food = Column(String, nullable=True)
    extra_food = Column(String, nullable=True)
    
    meal_price = Column(Integer, default=80)
