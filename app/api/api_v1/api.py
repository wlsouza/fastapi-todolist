from fastapi import APIRouter

from app.api.api_v1.endpoints import tasks


api_v1_router = APIRouter()

api_v1_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])