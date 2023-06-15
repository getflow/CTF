from fastapi import FastAPI, Depends

from app.routers.admin import admin_router
from app.routers.project import project_router
from app.security.basic_auth import basic_auth

app = FastAPI()

app.include_router(
    router=project_router,
    prefix="/api/v0",
    dependencies=[
        Depends(basic_auth)
    ]
)

app.include_router(
    router=admin_router,
    prefix="/api/v0"
)
