from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.database import Base, engine
import os
import time

from app.routes import auth, category, transaction, summary, catering

# Setup Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Finance Tracker Security Enhanced")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 1. Custom Middleware (Added first, so it runs "inner" for response)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    try:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response
    except Exception as e:
        # If an unhandled exception occurs, we still want to ensure security headers 
        # (though FastAPI's exception handler will usually catch this and return a 500)
        raise e

# 2. CORS Middleware (Added last, so it runs "outer" for response, ensuring headers even on errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://finance-tracker-frontend-0y2c.onrender.com",
        "https://finance-tracker-frontend-tfbl.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(category.router, prefix="/categories")
app.include_router(transaction.router, prefix="/transactions")
app.include_router(summary.router, prefix="/summary")
app.include_router(catering.router, prefix="/catering")