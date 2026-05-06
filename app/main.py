from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth, category, transaction

app = FastAPI(title="Finance Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(category.router, prefix="/categories")
app.include_router(transaction.router, prefix="/transactions")