from database import get_db
from app.cruds import google_api
from fastapi import APIRouter, Response, Request, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import app.cruds.login as login
import cruds.mail as crud_mail
import cruds.session_authentication as cruds_session_authentication
from app.cruds.google_api import decrypt_token
import cruds.user as cruds_user
from app.cruds.chatgpt import get_email_importance
import requests
from schemas.login import IsAuthResponse as IsAuthResponseSchema
from schemas.mail import MailCreate as MailCreateSchema


router = APIRouter()


@router.get('/login')
async def get_google_api(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if access_token:
        print("*"*100)
        mail_list = login.get_all_emails(access_token)
        for mail in mail_list:
            db_mail = crud_mail.get_message_by_mail_id(db, mail_id=mail[0])
            if db_mail:
                pass
            else:
                rank = get_email_importance(mail[4])
                print(rank)
                rank = str(rank)
                mail_create = MailCreateSchema(
                    mail_id=mail[0],
                    user_id="3",
                    title=mail[1],
                    your_name=mail[2],
                    your_mail_address=mail[3],
                    body=mail[4],
                    send_time=mail[5],
                    rank=rank,
                )
                crud_mail.create_message(db, mail_create)
        return Response(status_code=status.HTTP_200_OK)
    response = google_api.auth()
    return response

@router.get("/is_auth", response_model=IsAuthResponseSchema)
async def auth_callback(request: Request, response: Response, db: Session = Depends(get_db)):
    hash_session_id = request.cookies.get("session_id")
    if not hash_session_id:
        response = RedirectResponse(url="/login")
        return IsAuthResponseSchema(access = False)
    token_info_url = 'https://oauth2.googleapis.com/tokeninfo'
    print(hash_session_id, hash_session_id[2:-1])
    session_id = decrypt_token(hash_session_id[2:-1])
    user_id = cruds_session_authentication.get_user_id_by_session_id(db, session_id)
    hash_access_token = cruds_user.get_access_token_by_user_id(db=db, user_id=user_id)
    access_token = decrypt_token(hash_access_token[2:-1])
    params = {'access_token': access_token}
    response_mail = requests.get(token_info_url, params=params)
    if response_mail.status_code == 200:
        return IsAuthResponseSchema(access = True)
    else:
        response.delete_cookie("session_id", path="/")
        return IsAuthResponseSchema(access = False)

@router.get("/auth/callback", response_model=None)
async def auth_callback(response: Response, state: str,  code: str, scope: str, authuser: str, prompt: str, db: Session = Depends(get_db)):
    return google_api.set_cookies(code=code, db=db)


@router.get("/logout", response_model=None)
def logout(response: Response):
    # クッキーの削除
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token", path="/")
    return response
