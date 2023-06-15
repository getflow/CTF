import datetime
import uuid

from sqlmodel import SQLModel, Field

from app.models.user import User


class Commit(SQLModel, table=True):
    commit_id: str = Field(primary_key=True)
    parent_id: str = Field(foreign_key="commit.commit_id")
    author: uuid.UUID = Field(foreign_key=User.user_id)
    committer: uuid.UUID = Field(foreign_key=User.user_id)
    message: str
    created_at: datetime.datetime
    diff: str
