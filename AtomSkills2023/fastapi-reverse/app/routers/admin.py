from fastapi import APIRouter

from app.models.user import User
from app.schemas.user import SomeUser

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.post("/user", response_model=User)
async def create_user(user: SomeUser):
    return User.create_user(user=user)