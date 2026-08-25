from datetime import date, datetime, time
from enum import StrEnum

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.core.database import BaseModel, IdMixin


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Booking(BaseModel, IdMixin):
    __tablename__ = "bookings"

    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    booking_date: Mapped[date] = mapped_column(nullable=False)
    booking_time: Mapped[time] = mapped_column(nullable=False)
    guests: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[BookingStatus] = mapped_column(default=BookingStatus.ACTIVE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
