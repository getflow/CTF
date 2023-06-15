import uuid

from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/project/{project_id}/commit")
async def commit_list(project_id: uuid.UUID):
    pass


@app.post("/project/{project_id}/commit")
async def create_commit(project_id: uuid.UUID):
    pass


@app.get("/project/{project_id}/commit/{commit_id}")
async def get_commit(commit_id: str):
    pass


@app.get("/project/{project_id}/download")
async def download(project_id: uuid.UUID):
    pass


@app.post("/project")
async def create_project():
    pass
