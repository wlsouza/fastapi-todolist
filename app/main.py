import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_v1_router
from app.core.config import settings


app = FastAPI()

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
