from datetime import date, time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.booking.models import Booking, BookingStatus
from src.modules.core.base_repo import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def get(self, id: int) -> Booking | None:
        return await self._get(id)

    async def create(self, **kwargs) -> Booking:
        return await self._create(**kwargs)

    async def list(self, filter_date: date | None = None) -> list[Booking]:
        stmt = select(self.model)
        if filter_date is not None:
            stmt = stmt.where(self.model.booking_date == filter_date)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def cancel(self, id: int) -> Booking | None:
        booking = await self._get(id)
        if booking is None:
            return None
        return await self._update(id, {"status": BookingStatus.CANCELLED})

    async def is_slot_booked(self, booking_date: date, booking_time: time) -> bool:
        stmt = select(self.model).where(
            self.model.booking_date == booking_date,
            self.model.booking_time == booking_time,
            self.model.status == BookingStatus.ACTIVE,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
