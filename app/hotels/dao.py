import datetime
from datetime import date
from operator import or_

from sqlalchemy import select, and_, func

from app.bookings.models import Bookings
from app.dao.BaseDAO import BaseDAO
from app.database import async_session_maker, engine
from app.exceptions import DateFromBeforeDateToException, TooLongDatePeriodException
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_hotels_with_free_rooms(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        # Проверяем корректность пераданных дат
        if date_to <= date_from:
            raise DateFromBeforeDateToException
        if (date_to - date_from) > datetime.timedelta(days=30):
            raise TooLongDatePeriodException

        async with async_session_maker() as session:
            # WITH booked_rooms AS (
            # 	SELECT * FROM bookings WHERE
            # 	(bookings.date_from >= '2023-05-15' AND bookings.date_from <= '2023-06-14')
            # 	OR
            # 	(bookings.date_from <= '2023-05-15' AND bookings.date_to > '2023-05-15')
            # )
            booked_rooms = select(Bookings).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    )
                ),
            ).cte('booked_rooms')

            # SELECT hotels.id, hotels.name, hotels.location,
            # hotels.services, rooms.quantity AS rooms_quantity, rooms.image_id,
            # (rooms.quantity - COUNT(booked_rooms.id)) AS rooms_left from booked_rooms
            # LEFT JOIN rooms ON rooms.id=booked_rooms.room_id
            # LEFT JOIN hotels ON hotels.id=rooms.hotel_id
            # WHERE
            # hotels.location LIKE '%Алтай%'
            # GROUP BY rooms.id, hotels.id
            # HAVING COUNT(booked_rooms.id) < rooms.quantity
            get_hotels_available = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Rooms.quantity.label('rooms_quantity'),
                Rooms.image_id,
                (Rooms.quantity - func.count(booked_rooms.c.id)).label('rooms_left')
            ).select_from(booked_rooms).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).join(
                Hotels, Hotels.id == Rooms.hotel_id, isouter=True
            ).where(
                Hotels.location.like("%{}%".format(location))
            ).group_by(Rooms.id, Hotels.id).having(
                func.count(booked_rooms.c.id) < Rooms.quantity
            )

            # print(get_hotels_available.compile(engine, compile_kwargs={"literal_binds": True}))
            res = await session.execute(get_hotels_available)
            return res.mappings().all() # Решает проблему приведения типа для кэширования
