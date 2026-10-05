
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.connection import engine

from app.api.categories import router as categories_router
from app.api.resources import router as resources_router
from app.api.bookings import router as bookings_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="Campus Resource Booking Platform",
    description="API for booking campus resources",
    version="1.0.0",
)

app.include_router(categories_router)
app.include_router(resources_router)
app.include_router(bookings_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Campus Resource Booking Platform",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": "campus_booking_db",
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Check your MySQL settings.",
        )
