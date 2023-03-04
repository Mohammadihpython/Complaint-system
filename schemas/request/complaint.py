from pydantic import BaseModel


class ComplaintIn(BaseModel):
    title: str
    description: str
    amount: float
    encoded_photo: str
    extension: str
