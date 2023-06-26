from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelWithRoomsLeft

router = APIRouter(
    prefix='/hotels',
    tags=['Отели'],
)


@router.get('{location}')
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date
) -> list[SHotelWithRoomsLeft]:
    return await HotelDAO.find_hotels_with_free_rooms(location=location, date_from=date_from, date_to=date_to)


@router.get('/id/{hotel_id}')
async def get_hotel_info(hotel_id: int) -> SHotel:
    return await HotelDAO.find_one_or_none(id=hotel_id)
