import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_v1_router
from app.core.config import settings

from app.celery_worker import send_verification_email

app = FastAPI()

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/")
def im_alive():
    send_verification_email.delay("faranes767@whecode.com","Joandel","1232")
    return "I'am alive!"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
