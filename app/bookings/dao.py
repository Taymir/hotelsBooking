# dao - data access object
from sqlalchemy import select

from app.bookings.models import Bookings
from app.dao.BaseDAO import BaseDAO
from app.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings
