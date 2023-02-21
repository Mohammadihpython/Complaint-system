from datetime import datetime

from pydantic import BaseModel

from models import State


class ComplaintOut(BaseModel):
    id: int
    title: str
    description: str
    photo_url: str
    amount: float
    created_at: datetime
    status: State
