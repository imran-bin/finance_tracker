from apscheduler.schedulers.background import BackgroundScheduler
from db.database import SessionLocal
from db.models import User, Transaction
from services.whatsapp import send_whatsapp

scheduler = BackgroundScheduler()


def check_balance():
    db = SessionLocal()

    users = db.query(User).all()

    for u in users:
        txs = db.query(Transaction).filter(Transaction.user_id == u.id).all()

        balance = sum(t.amount for t in txs)

        if balance < 5000:
            send_whatsapp("+8801XXXXXXXXX", f"⚠ Low balance: {balance}")


def start_scheduler():
    scheduler.add_job(check_balance, "interval", hours=24)
    scheduler.start()