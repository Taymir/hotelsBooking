from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
import app.hotels.rooms.router

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


class HotelsSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
):
    hotels = [
        {
            "address": "Ул. Гагарина, 1, Алтай",
            "name": "Super hotel",
            "stars": 5,
        }
    ]
    return hotels
