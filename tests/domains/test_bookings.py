from datetime import date, timedelta

from httpx import AsyncClient


def make_booking_data(time_slot: str = "14:00:00", days_offset: int = 1) -> dict:
    return {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "booking_date": str(date.today() + timedelta(days=days_offset)),
        "booking_time": time_slot,
        "guests": 2,
    }


async def test_create_booking(client: AsyncClient):
    data = make_booking_data()
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == data["name"]
    assert body["phone"] == "+79991234567"
    assert body["status"] == "active"
    assert "id" in body


async def test_create_booking_invalid_phone(client: AsyncClient):
    data = make_booking_data()
    data["phone"] = "123"
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_past_date(client: AsyncClient):
    data = make_booking_data()
    data["booking_date"] = str(date.today() - timedelta(days=1))
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_invalid_time(client: AsyncClient):
    data = make_booking_data(time_slot="10:00:00")
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_guests_out_of_range(client: AsyncClient):
    data = make_booking_data()
    data["guests"] = 15
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_short_name(client: AsyncClient):
    data = make_booking_data()
    data["name"] = "A"
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_get_booking(client: AsyncClient):
    data = make_booking_data(time_slot="15:00:00")
    create_response = await client.post("/bookings/", json=data)
    assert create_response.status_code == 201
    booking_id = create_response.json()["id"]

    response = await client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["id"] == booking_id


async def test_get_booking_not_found(client: AsyncClient):
    response = await client.get("/bookings/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


async def test_list_bookings(client: AsyncClient):
    data = make_booking_data(time_slot="16:00:00")
    await client.post("/bookings/", json=data)

    response = await client.get("/bookings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


async def test_list_bookings_with_date_filter(client: AsyncClient):
    data = make_booking_data(time_slot="17:00:00")
    await client.post("/bookings/", json=data)

    tomorrow = str(date.today() + timedelta(days=1))
    response = await client.get(f"/bookings/?filter_date={tomorrow}")
    assert response.status_code == 200


async def test_cancel_booking(client: AsyncClient):
    data = make_booking_data(time_slot="18:00:00")
    create_response = await client.post("/bookings/", json=data)
    assert create_response.status_code == 201
    booking_id = create_response.json()["id"]

    response = await client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


async def test_cancel_booking_not_found(client: AsyncClient):
    response = await client.delete("/bookings/999999")
    assert response.status_code == 404


async def test_duplicate_slot_returns_409(client: AsyncClient):
    data = make_booking_data(time_slot="19:00:00")
    await client.post("/bookings/", json=data)
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 409


async def test_create_booking_name_with_digits(client: AsyncClient):
    data = make_booking_data()
    data["name"] = "Ivan123"
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_name_with_special_chars(client: AsyncClient):
    data = make_booking_data()
    data["name"] = "Иван@Иванов"
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_phone_starts_with_8(client: AsyncClient):
    data = make_booking_data()
    data["phone"] = "89991234567"
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 201
    assert response.json()["phone"] == "+79991234567"


async def test_create_booking_date_beyond_90_days(client: AsyncClient):
    data = make_booking_data()
    data["booking_date"] = str(date.today() + timedelta(days=91))
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_guests_zero(client: AsyncClient):
    data = make_booking_data()
    data["guests"] = 0
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_create_booking_guests_min(client: AsyncClient):
    data = make_booking_data()
    data["guests"] = 1
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 201
    assert response.json()["guests"] == 1


async def test_create_booking_time_boundary_22(client: AsyncClient):
    data = make_booking_data(time_slot="22:00:00")
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 201
    assert response.json()["booking_time"] == "22:00:00"


async def test_create_booking_time_23_rejected(client: AsyncClient):
    data = make_booking_data(time_slot="23:00:00")
    response = await client.post("/bookings/", json=data)
    assert response.status_code == 422


async def test_cancel_already_cancelled_booking(client: AsyncClient):
    data = make_booking_data(time_slot="20:00:00")
    create_response = await client.post("/bookings/", json=data)
    booking_id = create_response.json()["id"]

    await client.delete(f"/bookings/{booking_id}")
    response = await client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


async def test_list_bookings_empty_date_filter(client: AsyncClient):
    future_date = str(date.today() + timedelta(days=365))
    response = await client.get(f"/bookings/?filter_date={future_date}")
    assert response.status_code == 200
    assert response.json() == []
