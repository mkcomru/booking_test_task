from datetime import date

import structlog
from fastapi import APIRouter, status

from src.modules.booking.dependencies import BookingServiceDep
from src.modules.booking.schemas import BookingCreateRequest, BookingResponse

log = structlog.get_logger()

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(data: BookingCreateRequest, service: BookingServiceDep) -> BookingResponse:
    log.info(
        "booking.create",
        name=data.name,
        phone=data.phone,
        date=data.booking_date,
        time=data.booking_time,
        guests=data.guests,
    )
    booking = await service.create(data)
    log.info("booking.created", booking_id=booking.id, status=booking.status)
    return booking


@router.get("/", response_model=list[BookingResponse])
async def list_bookings(service: BookingServiceDep, filter_date: date | None = None) -> list[BookingResponse]:
    log.info("booking.list", filter_date=filter_date)
    bookings = await service.list(filter_date)
    log.info("booking.list.result", count=len(bookings))
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, service: BookingServiceDep) -> BookingResponse:
    log.info("booking.get", booking_id=booking_id)
    booking = await service.get(booking_id)
    log.info("booking.get.result", booking_id=booking.id, status=booking.status)
    return booking


@router.delete(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def cancel_booking(booking_id: int, service: BookingServiceDep) -> BookingResponse:
    log.info("booking.cancel", booking_id=booking_id)
    booking = await service.cancel(booking_id)
    log.info("booking.cancelled", booking_id=booking.id, status=booking.status)
    return booking
