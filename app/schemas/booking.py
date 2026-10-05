
from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
