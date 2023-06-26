from datetime import date

from sqlalchemy import select, or_, and_, func

from app.bookings.models import Bookings
from app.dao.BaseDAO import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_rooms_in_hotel(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
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

            # SELECT rooms.id, rooms.hotel_id, rooms.name,
            # rooms.description, rooms.services, rooms.price,
            # rooms.quantity, rooms.image_id,
            # (rooms.price * ('2023-06-14'::date - '2023-05-15'::date)) AS total_cost,
            # (rooms.quantity - COUNT(booked_rooms.id)) AS rooms_left from booked_rooms
            # LEFT JOIN rooms ON rooms.id=booked_rooms.room_id
            # LEFT JOIN hotels ON hotels.id=rooms.hotel_id
            # WHERE
            # hotels.id = 1
            # GROUP BY rooms.id, hotels.id
            # HAVING COUNT(booked_rooms.id) < rooms.quantity
            get_rooms_available = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * (date_to - date_from).days).label('total_cost'),
                (Rooms.quantity - func.count(booked_rooms.c.id)).label('rooms_left')
            ).select_from(booked_rooms).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).join(
                Hotels, Hotels.id == Rooms.hotel_id, isouter=True
            ).where(
                Hotels.id == hotel_id
            ).group_by(Rooms.id, Hotels.id).having(
                func.count(booked_rooms.c.id) < Rooms.quantity
            )

            print(get_rooms_available.compile(engine, compile_kwargs={"literal_binds": True}))
            res = await session.execute(get_rooms_available)
            return res.all()
