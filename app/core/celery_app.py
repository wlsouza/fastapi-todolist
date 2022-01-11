from celery import Celery

from app.core.config import settings

celery_app = Celery(broker=settings.BROKER_URI)
