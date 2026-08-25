from datetime import date, time, timedelta
from unittest.mock import AsyncMock

import pytest

from src.modules.booking.exceptions import BookingNotFoundError, SlotAlreadyBookedError
from src.modules.booking.models import Booking, BookingStatus
from src.modules.booking.schemas import BookingCreateRequest
from src.modules.booking.service import BookingService


def make_request(**overrides) -> BookingCreateRequest:
    defaults = {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "booking_date": date.today() + timedelta(days=1),
        "booking_time": time(14, 0),
        "guests": 2,
    }
    return BookingCreateRequest(**{**defaults, **overrides})


def make_booking(**overrides) -> Booking:
    defaults = {
        "id": 1,
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "booking_date": date.today() + timedelta(days=1),
        "booking_time": time(14, 0),
        "guests": 2,
        "status": BookingStatus.ACTIVE,
    }
    return Booking(**{**defaults, **overrides})


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(mock_session, mock_repo):
    svc = BookingService(mock_session)
    svc.repo = mock_repo
    return svc


async def test_service_create_booking(service, mock_repo):
    data = make_request()
    mock_repo.is_slot_booked.return_value = False
    mock_repo.create.return_value = make_booking()

    result = await service.create(data)

    assert result.status == BookingStatus.ACTIVE
    mock_repo.is_slot_booked.assert_awaited_once_with(data.booking_date, data.booking_time)
    mock_repo.create.assert_awaited_once()


async def test_service_create_booking_slot_busy(service, mock_repo):
    data = make_request()
    mock_repo.is_slot_booked.return_value = True

    with pytest.raises(SlotAlreadyBookedError):
        await service.create(data)


async def test_service_get_booking(service, mock_repo):
    booking = make_booking()
    mock_repo.get.return_value = booking

    result = await service.get(1)

    assert result.id == 1
    mock_repo.get.assert_awaited_once_with(1)


async def test_service_get_booking_not_found(service, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(BookingNotFoundError):
        await service.get(999)


async def test_service_list_all(service, mock_repo):
    mock_repo.list.return_value = [make_booking(), make_booking(id=2)]

    result = await service.list()

    assert len(result) == 2
    mock_repo.list.assert_awaited_once_with(None)


async def test_service_list_by_date(service, mock_repo):
    mock_repo.list.return_value = [make_booking()]
    target_date = date.today() + timedelta(days=1)

    result = await service.list(filter_date=target_date)

    assert len(result) == 1
    mock_repo.list.assert_awaited_once_with(target_date)


async def test_service_cancel_booking(service, mock_repo):
    booking = make_booking(status=BookingStatus.CANCELLED)
    mock_repo.cancel.return_value = booking

    result = await service.cancel(1)

    assert result.status == BookingStatus.CANCELLED
    mock_repo.cancel.assert_awaited_once_with(1)


async def test_service_cancel_booking_not_found(service, mock_repo):
    mock_repo.cancel.return_value = None

    with pytest.raises(BookingNotFoundError):
        await service.cancel(999)
