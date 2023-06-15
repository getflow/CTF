import hashlib
import uuid

from fastapi import APIRouter, Depends
from pydantic.typing import List

from app.models.commit import Commit
from app.models.project import Project
from app.models.user import User
from app.schemas.commit import SomeCommit
from app.schemas.project import SomeProject
from app.security.basic_auth import basic_auth

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/{project_id}/commit", response_model=List[Commit])
async def commit_list(project_id: uuid.UUID):
    return Commit.get_commits(project_id=project_id)


@project_router.post("/{project_id}/commit", response_model=Commit)
async def create_commit(project_id: uuid.UUID, commit: SomeCommit):
    return Commit.create_commit(project_id=project_id, commit=commit)


@project_router.get("/{project_id}/commit/{commit_id}", response_model=Commit)
async def get_commit(commit_id: str):
    return Commit.get_commit(commit_id=commit_id)


@project_router.get("/{project_id}/head", response_model=Commit)
async def head(project_id: uuid.UUID):
    return Commit.get_head(project_id=project_id)


@project_router.post("/", response_model=Project)
async def create_project(project: SomeProject, user: User = Depends(basic_auth)):
    return Project.create_project(project=project, owner_id=user.user_id)


@project_router.get("/flag", response_model=str)
async def get_flag(data: str):
    return "flag{%s}" % hashlib.md5(data.encode("utf-8")).hexdigest()
