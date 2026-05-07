import os
from sqlalchemy import create_engine
from app.core.database import Base, SQLALCHEMY_DATABASE_URL
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category

def reset_database():
    print(f"Connecting to: {SQLALCHEMY_DATABASE_URL}")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Drop all tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Recreate all tables
    print("Recreating tables (Fresh Start)...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Success! Your database is now completely empty.")

if __name__ == "__main__":
    confirm = input("ARE YOU SURE? This will delete ALL users and data. (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Reset cancelled.")
