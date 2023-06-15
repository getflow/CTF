import datetime
import uuid

from sqlmodel import SQLModel, Field

from app.database import session


class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    registered_at: datetime.datetime
    password: str

    @staticmethod
    def get_user(user_id: uuid.UUID) -> "User":
        with session() as dbs:
            user = dbs.get(User, user_id)
            return user
