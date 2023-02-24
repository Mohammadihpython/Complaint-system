from datetime import datetime, timedelta
from typing import Optional
from db import database
import jwt
from config import settings
from datetime import timezone
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from models import user, RoleType


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.now(timezone.utc) + timedelta(minutes=120),
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
            payload = jwt.decode(
                res.credentials, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            """ ComplaintSystem user data in request state to use globally"""
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(401, "token is exp") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(401, "Invalid token") from e


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if request.state.user["role"] != RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if request.state.user["role"] != RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if request.state.user["role"] != RoleType.admin:
        raise HTTPException(403, "Forbidden")


# used DRY concept
# def check_role(request: Request, role_type: RoleType):
#     if not request.state.user["role"] == role_type:
#         raise HTTPException(403, "Forbidden")

# is_complainer = lambda request: check_role(request, RoleType.complainer)
# is_approver = lambda request: check_role(request, RoleType.approver)
# is_admin = lambda request: check_role(request, RoleType.admin)
