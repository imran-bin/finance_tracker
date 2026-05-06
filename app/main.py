from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import Base, engine, get_db
from models import Transaction
from fastapi.middleware.cors import CORSMiddleware

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# allow frontend (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "Finance Tracker API running"}

# ➕ Add transaction
@app.post("/add")
def add(title: str, amount: float, type: str, db: Session = Depends(get_db)):
    tx = Transaction(title=title, amount=amount, type=type)
    db.add(tx)
    db.commit()
    return {"msg": "added"}

# 📊 Get all transactions
@app.get("/all")
def all_tx(db: Session = Depends(get_db)):
    return db.query(Transaction).all()