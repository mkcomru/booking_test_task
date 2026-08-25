from fastapi import FastAPI, JSONResponse
from fastapi.exceptions import RequestValidationError

from src.modules.booking.exceptions import BookingNotFoundError, SlotAlreadyBookedError


async def booking_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Booking not found"})


async def slot_already_booked_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": "Slot already booked"})


async def validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BookingNotFoundError, booking_not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(SlotAlreadyBookedError, slot_already_booked_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_handler)  # type: ignore[arg-type]
