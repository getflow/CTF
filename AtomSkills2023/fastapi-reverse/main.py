import uuid

from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/{project_id}/commit")
async def commit_list(project_id: uuid.UUID):
    pass


@app.post("/{project_id}/commit")
async def create_commit(project_id: uuid.UUID):
    pass


@app.get("/{project_id}/commit/{commit_id}")
async def get_commit(commit_id: uuid.UUID):
    pass


@app.get("/{project_id}/mr")
async def mr_list(project_id: uuid.UUID):
    pass


@app.post("/{project_id}/mr/{mr_id}")
async def mr(project_id: uuid.UUID, mr_id: uuid.UUID):
    pass


@app.post("/{project_id}/mr")
async def create_mr(project_id: uuid.UUID):
    pass


@app.get("/{project_id}/download")
async def download(project_id: uuid.UUID):
    pass


@app.get("/{project_id}")
async def view(project_id: uuid.UUID):
    return HTMLResponse("""<html>
    <head>
    </head>
    <body>
    </body>
</html>""")
