from fastapi import APIRouter

from app.api.api_v1.endpoints import login


api_v1_router = APIRouter()

api_v1_router.include_router(login.router, prefix="/login", tags=["login"])
# api_v1_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])