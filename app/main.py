from fastapi import FastAPI
from routers import auth, finance
from services.scheduler import start_scheduler
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(finance.router, prefix="/finance")

start_scheduler()