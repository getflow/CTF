import datetime
import uuid

from sqlmodel import SQLModel, Field

from app.database import session
from app.models.user import User
from app.schemas.project import SomeProject


class Project(SQLModel, table=True):
    project_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    description: str
    created_at: datetime.datetime
    owner_id: uuid.UUID = Field(foreign_key=User.user_id)

    @staticmethod
    def create_project(owner_id: uuid.UUID, project: SomeProject) -> "Project":
        with session() as dbs:
            new_project = Project(
                name=project.name,
                description=project.description,
                created_at=datetime.datetime.now(),
                owner_id=owner_id
            )
            dbs.add(new_project)
            dbs.commit()
            return new_project
