from fastapi import APIRouter

router = APIRouter()

@router.post("/access-token")
def login_access_token():
    pass