import datetime
import uuid

from pydantic.typing import List
from sqlmodel import SQLModel, Field, select, col

from app.database import session
from app.models.project import Project
from app.models.user import User
from app.schemas.commit import SomeCommit


class Commit(SQLModel, table=True):
    commit_id: str = Field(primary_key=True)
    parent_id: str = Field(foreign_key="commit.commit_id")
    project_id: uuid.UUID = Field(foreign_key=Project.project_id)
    author: uuid.UUID = Field(foreign_key=User.user_id)
    message: str
    created_at: datetime.datetime
    diff: str

    @staticmethod
    def get_commits(project_id: uuid.UUID) -> List["Commit"]:
        with session() as dbs:
            return dbs.exec(
                select(Commit)
                .where(Commit.project_id == project_id)
                .order_by(Commit.created_at)
            ).fetchall()

    @staticmethod
    def get_commit(commit_id: str) -> "Commit":
        with session() as dbs:
            return dbs.get(Commit, commit_id)

    @staticmethod
    def get_head(project_id: uuid.UUID) -> "Commit":
        with session() as dbs:
            return dbs.exec(
                select(Commit)
                .where(Commit.project_id == project_id)
                .order_by(col(Commit.created_at).desc())
                .limit(1)
            ).first()

    @staticmethod
    def create_commit(project_id: uuid.UUID, author_id: uuid.UUID, commit: SomeCommit) -> "Commit":
        now = datetime.datetime.now()
        print(str(hash(frozenset(dict(
                    partial_hash=commit.partial_hash,
                    created_at=now,
                    author_id=author_id
                ).items()))))

        with session() as dbs:
            new_commit = Commit(
                commit_id=str(hash(frozenset(dict(
                    partial_hash=commit.partial_hash,
                    # created_at=datetime.datetime.now(),
                    created_at=now,
                    author_id=author_id
                ).items()))),
                parent_id=commit.parent_id,
                author=author_id,
                message=commit.message,
                created_at=now,
                project_id=project_id,
            )
            dbs.add(new_commit)
            dbs.commit()
            return new_commit
