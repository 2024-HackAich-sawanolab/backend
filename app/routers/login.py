import cruds.user as crud
from database import get_db
from fastapi import APIRouter
from schemas.login import GoogleLogin


router = APIRouter()

@router.get('/login', response_model=GoogleLogin)
async def get_google_api():
    return "Hello"