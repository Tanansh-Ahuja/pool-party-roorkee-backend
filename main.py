<<<<<<< HEAD
from fastapi import FastAPI
from routers import customers, bookings, payments, monthly_packages,blocked_dates, group_members , settings, earnings, notice, auth
import logging
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN")

app = FastAPI(
    title="Pool Party Roorkee API",
    version="1.0.0" 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"{ALLOW_ORIGIN}"],  # or ["*"] for all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(monthly_packages.router)
app.include_router(blocked_dates.router)
app.include_router(group_members.router)
app.include_router(settings.router)
app.include_router(earnings.router)
app.include_router(notice.router)
app.include_router(auth.router)

# Run with uvicorn
# uvicorn main:app --reload
=======
from fastapi import FastAPI
from routers import customers, bookings, payments, monthly_packages,blocked_dates, group_members , settings, earnings, notice, auth
import logging
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN")

app = FastAPI(
    title="Pool Party Roorkee API",
    version="1.0.0" 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"{ALLOW_ORIGIN}"],  # or ["*"] for all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(monthly_packages.router)
app.include_router(blocked_dates.router)
app.include_router(group_members.router)
app.include_router(settings.router)
app.include_router(earnings.router)
app.include_router(notice.router)
app.include_router(auth.router)

# Run with uvicorn
# uvicorn main:app --reload
>>>>>>> origin/main
