import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session
from typing import List
from schemas.mail import MailAllResponse as MailAllResponseSchema, MailDetail as MailDetailSchema, MailCreate as MailCreateSchema, MailSendRequest as MailSendRequestSchema
import cruds.mail as crud_mail
import cruds.mail_send_flag as crud_send_flag
from app.cruds.mail_send_flag import store_send_flag_by_mail_id as store_send_flag
import app.cruds.login as login
from app.cruds.chatgpt import get_email_importance
from fastapi.responses import RedirectResponse
from app.cruds import google_api
from schemas.login import IsAuthResponse as IsAuthResponseSchema
import cruds.session_authentication as cruds_session_authentication
from app.cruds.google_api import decrypt_token
import cruds.user as cruds_user
from app.cruds.chatgpt import get_email_importance


router = APIRouter()

@router.get('/all', response_model=List[MailAllResponseSchema])
async def get_message_by_user_id(request: Request, db: Session = Depends(get_db)):
    
    hash_session_id = request.cookies.get("session_id")
    if not hash_session_id:
        response = RedirectResponse(url="/login")
        return IsAuthResponseSchema(access = False)
    token_info_url = 'https://oauth2.googleapis.com/tokeninfo'
    session_id = decrypt_token(hash_session_id[2:-1])
    user_id = cruds_session_authentication.get_user_id_by_session_id(db, session_id)
    hash_access_token = cruds_user.get_access_token_by_user_id(db=db, user_id=user_id)
    access_token = decrypt_token(hash_access_token[2:-1])
    if access_token:
        mail_list = login.get_all_emails(access_token)
        for mail in mail_list:
            db_mail = crud_mail.get_message_by_mail_id(db, mail_id=mail[0])
            if db_mail:
                pass
            else:
                rank = get_email_importance(mail[4])
                rank = str(rank)
                mail_create = MailCreateSchema(
                    mail_id = mail[0],
                    user_id = user_id,
                    title = mail[1],
                    your_name = mail[2],
                    your_mail_address = mail[3],
                    body = mail[4],
                    send_time = mail[5],
                    rank = rank,
                )
                crud_mail.create_message(db, mail_create)
        return crud_mail.get_message_by_user_id(db=db, user_id=user_id)
    response = google_api.auth()
    return response



@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(mail_id: str, db: Session = Depends(get_db)):
    return crud_mail.get_message_by_mail_id(db=db, mail_id=mail_id)


@router.get('/{mail_id}/send_flag')
async def store_send_flag_by_mail_id(mail_id: str, db: Session = Depends(get_db)):
    store_send_flag(db=db, mail_id=mail_id)
    return Response(status_code=status.HTTP_200_OK)

@router.post('/send')
async def send_mail_by_access_token(request: Request, message: MailSendRequestSchema, db: Session = Depends(get_db)):
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
    crud_mail.send_mail_by_access_token(message, access_token)
    store_send_flag(db=db, mail_id=message.mail_id)
    crud_mail.save_answer_by_access_token(db=db, mail_id=message.mail_id, answer=message.body)
    return Response(status_code=status.HTTP_200_OK)

