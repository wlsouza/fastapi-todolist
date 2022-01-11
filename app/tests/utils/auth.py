from datetime import timedelta
from typing import Dict

from app import models
from app.core.security import create_jwt_token


def get_user_token_headers(user: models.User) -> Dict[str, str]:
    token = create_jwt_token(subject=user.id)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def get_expired_user_token_headers(user: models.User) -> Dict[str, str]:
    expire_delta = timedelta(minutes=-1)
    token = create_jwt_token(subject=user.id, expires_delta=expire_delta)
    headers = {"Authorization": f"Bearer {token}"}
    return headers
