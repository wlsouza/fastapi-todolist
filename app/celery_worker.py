import asyncio
from fastapi_mail import FastMail, MessageSchema

from app.core.celery_app import celery_app
from app.core.config import settings

@celery_app.task
def send_verification_email(email_to:str, first_name:str, token:str):
    
    verification_link = f"https://github.com/wlsouza/fastapi-todolist" #TODO: insert link to frontend page resolve it.

    message = MessageSchema(
        subject = "FastAPI-TodoList Email Verification",
        recipients =[email_to],
        template_body = {
            "first_name": first_name,
            "verification_link": verification_link
        }
    )

    fm = FastMail(settings.EMAIL_CONNECTION_CONFIG)
    asyncio.run( 
        fm.send_message(message, template_name="verification_email.html")
    )



