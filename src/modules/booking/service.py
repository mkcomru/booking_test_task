from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.booking.exceptions import BookingNotFoundError, SlotAlreadyBookedError
from src.modules.booking.models import Booking
from src.modules.booking.repository import BookingRepository
from src.modules.booking.schemas import BookingCreateRequest


class BookingService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.repo = BookingRepository(session)

    async def create(self, data: BookingCreateRequest) -> Booking:
        is_booked = await self.repo.is_slot_booked(data.booking_date, data.booking_time)
        if is_booked:
            raise SlotAlreadyBookedError
        booking = await self.repo.create(**data.model_dump())
        await self._session.commit()
        return booking

    async def get(self, booking_id: int) -> Booking:
        booking = await self.repo.get(booking_id)
        if booking is None:
            raise BookingNotFoundError
        return booking

    async def list(self, filter_date: date | None = None) -> list[Booking]:
        return await self.repo.list(filter_date)

    async def cancel(self, booking_id: int) -> Booking:
        booking = await self.repo.cancel(booking_id)
        if booking is None:
            raise BookingNotFoundError
        await self._session.commit()
        return booking
