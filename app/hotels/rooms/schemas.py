from datetime import date
from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    class Config:
        orm_mode = True