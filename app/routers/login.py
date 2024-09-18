from database import get_db
from cruds import googleAPI
from fastapi import APIRouter, Response, Request, status

router = APIRouter()
REDIRECT_URI = "http://localhost:8888/auth/callback"
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']


@router.get('/login')
async def get_google_api(request: Request):
    access_token = request.cookies.get("access_token")
    #access_tokenがあれば返すだけ
    if access_token:
        return "OK"
    #ログイン処理の実行
    response = googleAPI.auth()
    return response

@router.get("/auth/callback", response_model=None)
async def auth_callback(response: Response, state: str,  code: str, scope: str, authuser: str, prompt: str):
    return googleAPI.set_cookies(code=code)