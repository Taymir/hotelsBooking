from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked, BookingNotFoundException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all_with_rooms(user_id=user.id)


@router.post('/add')
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete('/{booking_id}')
async def remove_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    if not booking or booking.user_id != user.id:
        raise BookingNotFoundException
    return await BookingDAO.remove(booking_id)

