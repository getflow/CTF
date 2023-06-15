import datetime
import hashlib
import uuid

from pydantic.typing import Optional
from sqlalchemy import func
from sqlmodel import SQLModel, Field, select

from app.database import session
from app.schemas.user import SomeUser


class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    registered_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    password: str

    @staticmethod
    def get_user(user_id: uuid.UUID) -> "User":
        with session() as dbs:
            user = dbs.get(User, user_id)
            return user

    @staticmethod
    def create_user(user: SomeUser) -> "User":
        with session() as dbs:
            user = User(
                name=user.name,
                password=hashlib.md5(user.password.encode("utf-8")).hexdigest()
            )
            dbs.add(user)
            dbs.commit()
            return user
