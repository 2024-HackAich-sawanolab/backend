import secrets
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
import requests
from fastapi import HTTPException
from .. import env
import base64
import json
from cryptography.fernet import Fernet
from ..cruds import user as UserCruds
from ..cruds import session_authentication as SessionAuthenticationCruds
from sqlalchemy.orm import Session
from schemas import user as UserSchemas
from schemas import session_authentication as SessionAuthenticationSchemas
import datetime



SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
]


def auth():
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": env.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "redirect_uri": env.REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    auth_url = f"{env.AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    response = RedirectResponse(url=auth_url)
    return response


def get_access_token(code: str) -> dict:
    data = {
        "code": code,
        "client_id": env.GOOGLE_CLIENT_ID,
        "client_secret": env.GOOGLE_CLIENT_SECRET,
        "redirect_uri": env.REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(env.TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="アクセストークンの取得に失敗しました。")

    return response.json()

def decode_id_token(id_token):
    try:
        parts = id_token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT structure")
        
        payload_b64 = parts[1]
        
        padding = '=' * (-len(payload_b64) % 4)
        payload_b64 += padding
        decoded_bytes = base64.urlsafe_b64decode(payload_b64)
        
        payload = json.loads(decoded_bytes)
        return payload
    except Exception as e:
        print(f"Failed to decode id_token: {e}")
        return None

def encrypt_token(token: str,) -> bytes:
    fernet = Fernet(env.TOKEN_KEY.encode('utf-8'))
    token_bytes = token.encode('utf-8')
    encrypted_token = fernet.encrypt(token_bytes)
    return encrypted_token

def decrypt_token(encrypted_token: str) -> str:
    fernet = Fernet(env.TOKEN_KEY.encode('utf-8'))
    decrypted_bytes = fernet.decrypt(encrypted_token.encode('utf-8'))
    decrypted_token = decrypted_bytes.decode('utf-8')
    return decrypted_token

def calculate_expiration(duration_seconds: int) -> datetime.datetime:
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(seconds=duration_seconds)
    return expiration_time


def set_cookies(code: str, db: Session):
    token_data = get_access_token(code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")
    token_type = token_data.get("token_type")
    id_token = token_data.get("id_token")
    payload  = decode_id_token(id_token)
    create_user = UserSchemas.UserCreate(
        user_name = payload.get("name"),
        access_token = str(encrypt_token(access_token)),
        refresh_token = str(encrypt_token(refresh_token)),
        access_token_expiry = calculate_expiration(int(expires_in))
    )
    user_id = UserCruds.store_user(
        db=db,
        user=create_user
    )
    
    session_authentication=SessionAuthenticationSchemas.SessionAuthenticationCreate(
        user_id=user_id,
        expires_at=calculate_expiration(30*60)
    )
    session_id = SessionAuthenticationCruds.store_session(
        db=db,
        session_authentication=session_authentication
    )
    hash_session_id = encrypt_token(session_id)

    response = RedirectResponse(url="http://localhost:5173/")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )

    response.set_cookie(
        key="session_id",
        value=hash_session_id,
        httponly=True,  # JavaScriptからアクセス不可
        secure=True,    # HTTPSを使用している場合はTrueに設定
        samesite="strict", # 必要に応じて'Strict'や'None'に設定
    )

    return response
