import datetime
import uuid

from sqlmodel import SQLModel


class User(SQLModel, table=True):
    user_id: uuid.UUID
    name: str
    registered_at: datetime.datetime
