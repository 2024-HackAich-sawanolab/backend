import secrets
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
import requests
from fastapi import HTTPException


SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
REDIRECT_URI = "http://localhost:8888/auth/callback"
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
def auth():
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "redirect_uri": REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    auth_url = f"{AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    response = RedirectResponse(url=auth_url)
    return response

#認可コードからアクセストークンを取得
def get_access_token(code: str) -> dict:
    """
    認可コードを使用してアクセストークンを取得する関数。
    """
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="アクセストークンの取得に失敗しました。")

    return response.json()

def set_cookies(code: str):
    token_data = get_access_token(code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")  # リフレッシュトークン
    expires_in = token_data.get("expires_in")  # アクセストークンの有効期限（秒）
    token_type = token_data.get("token_type")
    response = RedirectResponse(url="/login")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True, # HttpOnly
    )
    return response