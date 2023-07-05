import json

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    *[(4, "2030-05-01", "2030-05-15", 200)]*8,
    (4, "2030-05-01", "2030-05-15", 409),
    (4, "2030-05-01", "2030-05-15", 409)
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code,
                                   authenticated_ac: AsyncClient):
    response = await authenticated_ac.post('/bookings/add', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
    })
    assert response.status_code == status_code


async def test_get_and_delete_all_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get('/bookings')
    assert response.status_code == 200
    bookings = response.json()
    assert len(bookings) > 0

    for b in bookings:
        response = await authenticated_ac.delete(f'/bookings/{b["id"]}')

    response = await authenticated_ac.get('/bookings')
    assert response.status_code == 200
    bookings = response.json()
    assert len(bookings) == 0


async def test_add_read_remove_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post('/bookings/add', params={
        'room_id': 3,
        'date_from': '2025-05-05',
        'date_to': '2025-05-10',
    })
    assert response.status_code == 200
    booking_id = response.json()['id']

    response = await authenticated_ac.get('/bookings')
    assert response.status_code == 200
    bookings = response.json()
    assert any(b['id'] == booking_id for b in bookings)

    response = await authenticated_ac.delete(f'/bookings/{booking_id}')
    assert response.status_code == 200

    response = await authenticated_ac.get('/bookings')
    assert response.status_code == 200
    bookings = response.json()
    assert all(b['id'] != booking_id for b in bookings)
