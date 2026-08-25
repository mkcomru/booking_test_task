from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.booking.service import BookingService
from src.modules.core.database import get_db


def get_booking_service(session: AsyncSession = Depends(get_db)) -> BookingService:  # noqa: B008
    return BookingService(session)


BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
