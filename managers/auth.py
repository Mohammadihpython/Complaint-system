from datetime import datetime, timedelta
from typing import Optional
from db import database
import jwt
from config import settings
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from models import user


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        except Exception as ex:
            """log the exception"""
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, settings.SECRET_KEY, algorithms=["HS256"])
            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            """ ComplaintSystem user data in request state to use globally"""
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "token is exp")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")
