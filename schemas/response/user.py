import string

from models import RoleType
from schemas.request.user import UserBase


class UserOut(UserBase):
    id: int
    first_name: str
    lastname: str
    phone_number: str
    role: RoleType
    iban: str
