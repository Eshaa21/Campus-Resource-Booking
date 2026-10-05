
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Booking
from app.schemas.booking import BookingCreate

from app.models import Booking, Resource
from app.auth.dependencies import get_current_user
from app.auth.dependencies import get_current_admin
from datetime import datetime, timezone

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    
    if booking.start_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Booking start time cannot be in the past",
        )

    if booking.end_time <= booking.start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time",
        )

    
    duration = booking.end_time - booking.start_time

    if duration.total_seconds() > 8 * 60 * 60:
        raise HTTPException(
            status_code=400,
            detail="Booking cannot exceed 8 hours",
        )
    
    resource = db.query(Resource).filter(
        Resource.id == booking.resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    
    overlapping_booking = db.query(Booking).filter(
        Booking.resource_id == booking.resource_id,
        Booking.status != "cancelled",
        Booking.start_time < booking.end_time,
        Booking.end_time > booking.start_time,
    ).first()


    if overlapping_booking:
        raise HTTPException(
            status_code=400,
            detail="Resource is already booked for this time slot",
        )

    new_booking = Booking(
        user_id=current_user.id,
        resource_id=booking.resource_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@router.get("/")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()



@router.patch("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if status not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be approved or rejected",
        )

    booking.status = status
    db.commit()
    db.refresh(booking)

    return booking


@router.get("/my-bookings")
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()

    return bookings



@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id,
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if booking.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Booking is already cancelled",
        )

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "status": booking.status,
    }
