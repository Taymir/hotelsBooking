from datetime import date

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoom
from app.hotels.router import router


@router.get('{hotel_id}/rooms')
async def get_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date,
) -> list[SRoom]:
    return await RoomsDAO.find_rooms_in_hotel(hotel_id, date_from, date_to)
