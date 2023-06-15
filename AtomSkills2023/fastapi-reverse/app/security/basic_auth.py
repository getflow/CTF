import hashlib
import uuid

from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic.typing import Optional
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.user import User


class BasicAuth(HTTPBasic):
    async def __call__(self, request: Request) -> User:
        authorization = await super().__call__(request)

        user_id = authorization.username
        user = User.get_user(user_id=uuid.UUID(user_id))
        if (
            not user or hashlib.md5(authorization.password).hexdigest() != user.password  # noqa: W503
        ):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        return user


basic_auth = BasicAuth()
