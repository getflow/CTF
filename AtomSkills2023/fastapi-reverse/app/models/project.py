import datetime
import uuid

from sqlmodel import SQLModel, Field

from app.models.user import User


class Project(SQLModel, table=True):
    project_id: uuid.UUID = Field(primary_key=True)
    name: str
    description: str
    created_at: datetime.datetime
    owner_id: uuid.UUID = Field(foreign_key=User.user_id)
