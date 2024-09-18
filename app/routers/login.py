from database import get_db
from app.cruds import google_api
from fastapi import APIRouter, Response, Request, status

router = APIRouter()

@router.get('/login')
async def get_google_api(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token:
        return "OK"
    response = google_api.auth()
    return response

@router.get("/auth/callback", response_model=None)
async def auth_callback(response: Response, state: str,  code: str, scope: str, authuser: str, prompt: str):
    return google_api.set_cookies(code=code)