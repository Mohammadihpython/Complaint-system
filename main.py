import re
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import databases
import sqlalchemy
import jwt
import uvicorn
from passlib.context import CryptContext
from pydantic import BaseModel, validator, EmailStr, BaseSettings

DATABASE_URL = "postgresql://postgres:postgre@localhost:5432/posgres"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(250)),
    sqlalchemy.Column("last_name", sqlalchemy.String(250)),
    sqlalchemy.Column("phone_number", sqlalchemy.String(13), unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),

    sqlalchemy.Column("created_time", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "modified_at", sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now()),
),


def phone_number_validation(value):
    if re.search("^(\\+98|0)?9\\d{9}$", value):
        return True
    else:
        return False


class PhoneNumberValidate(str):
    @classmethod
    def __get_validate__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            phone_number_validation(v)
            return v
        except ValueError:
            raise HTTPException(404, "phone_number is not valid")


class UserSign(BaseModel):
    phone_number: str
    email: EmailStr
    first_name: str
    last_name: str

    @validator("phone_number")
    def validate_email(cls, v):
        try:
            phone_number_validation(v)
            return v
        except ValueError:
            raise HTTPException(404, "phone_number is not valid")


class UserSignIn(UserSign):
    password: str


class UserSignOut(UserSign):
    pass


class Settings(BaseSettings):
    JWT_SECRET: str

    class Config:
        env_file = '.env'


settings = Settings()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


""" jwt section"""


def create_access_token(user):
    try:
        payload = {"sub": user["id"], "exp": datetime.utcnow() + timedelta(minutes=120)}
        return jwt.encode(payload, settings("JWT_SEcRET"), algorithm="HS256")
    except Exception as ex:
        raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(res.credentials, settings.SECRET_KEY, algorithms=["HS256"])
            user = await  database.fetch_one(users.select().where(users.c.id == payload["sub"]))
            # add user to global
            request.state.user = user
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "invalid token")


oauth_schema = CustomHTTPBearer()


@app.get("/clothes", dependencies=[Depends(oauth_schema)])
async def get_all_clothes():
    return []


@app.post("/register/")
async def create_user(user: UserSignIn):
    user.password = pwd_context.hash(user.password)
    query = users.insert().values(**user.dict())
    _id = await database.execute(query)
    created_user = await database.fetch_one(users.select().where(users.c.id == _id))
    token = create_access_token(created_user)
    return {'token': token}


if __name__ == "__main__":
    uvicorn.run("main:app")
