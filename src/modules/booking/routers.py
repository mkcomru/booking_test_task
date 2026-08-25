from datetime import date

from fastapi import APIRouter, status

from src.modules.booking.dependencies import BookingServiceDep
from src.modules.booking.schemas import BookingCreateRequest, BookingResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(data: BookingCreateRequest, service: BookingServiceDep) -> BookingResponse:
    booking = await service.create(data)
    return booking


@router.get("/", response_model=list[BookingResponse])
async def list_bookings(service: BookingServiceDep, filter_date: date | None = None) -> list[BookingResponse]:
    return await service.list(filter_date)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, service: BookingServiceDep) -> BookingResponse:
    return await service.get(booking_id)


@router.delete(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def cancel_booking(booking_id: int, service: BookingServiceDep) -> BookingResponse:
    return await service.cancel(booking_id)
