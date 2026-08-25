import re
from datetime import date, time, timedelta

from pydantic import BaseModel, Field, field_validator


class BookingCreateRequest(BaseModel):
    name: str = Field(min_length=2, pattern=r"^[a-zA-Zа-яА-ЯёЁ\- ]+$")  # noqa: RUF001
    phone: str
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11 or digits[0] not in ("7", "8"):
            raise ValueError("Введите корректный номер: +7 или 8, затем 10 цифр")
        return "+7" + digits[1:]

    @field_validator("booking_date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        today = date.today()
        max_date = today + timedelta(days=90)
        if v < today:
            raise ValueError("Дата не может быть раньше сегодняшнего дня")
        if v > max_date:
            raise ValueError("Дата не может быть позже 90 дней")
        return v

    @field_validator("booking_time")
    @classmethod
    def validate_time(cls, v: time) -> time:
        if not 12 <= v.hour <= 22 or v.minute != 0:
            raise ValueError("Доступные слоты: c 12:00 до 22:00 c шагом 1 час")
        return v


class BookingResponse(BaseModel):
    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: str

    model_config = {"from_attributes": True}
