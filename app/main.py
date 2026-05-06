from fastapi import FastAPI
from app.core.database import Base, engine

from app.routes import auth, category, transaction, summary

app = FastAPI(title="Finance Tracker")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(category.router, prefix="/categories")
app.include_router(transaction.router, prefix="/transactions")
app.include_router(summary.router, prefix="/summary")