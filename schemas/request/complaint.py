from pydantic import BaseModel


class ComplaintIn(BaseModel):
    title: str
    description: str
    photo_url: str
    amount: float
