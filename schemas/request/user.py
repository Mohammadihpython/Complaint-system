from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserRegisterIn(UserBase):
    password: str
    phone_number: str
    first_name: str
    last_name: str
    iban: str


class UserLoginIn(UserBase):
    password: str
