from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('location, date_from, date_to, status_code', [
    ('Алтай', '2023-05-15', '2023-06-14', 200),  # Все ок
    ('Алтай', '2023-06-15', '2023-05-14', 400),  # Дата начала позже даты конца
    ('Алтай', '2023-05-15', '2023-06-16', 400),  # Период больше месяца
    ('Алтай', '2023-05-15', '2023-05-15', 400),  # Период меньше дня
])
async def test_get_hotels(location, date_from, date_to, status_code,
                          ac: AsyncClient):
    response = await ac.get(f'/hotels/{location}', params={
        'date_from': date_from,
        'date_to': date_to,
    })
    assert response.status_code == status_code
