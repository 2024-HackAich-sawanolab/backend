import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.mail import MailAllResponse as MailAllResponseSchema, MailDetail as MailDetailSchema, MailCreate as MailCreateSchema
import app.cruds.login as login
import cruds.mail as crud_mail
from app.cruds.chatgpt import get_email_importance
router = APIRouter()
from datetime import datetime

fake_mails = [
    {
        "mail_id": "1",
        "title": "Welcome Email",
        "body": "Welcome to our service! We're glad to have you.",
        "your_name": "Alice Smith",
        "your_mail_address": "alice.smith@example.com",
        "rank": "1",
        "send_time": str(datetime(2024, 9, 14, 12, 30)),
        "send_flag": True
    },
    {
        "mail_id": "2",
        "title": "Password Reset",
        "body": "Click the link below to reset your password.",
        "your_name": "Bob Johnson",
        "your_mail_address": "bob.johnson@example.com",
        "rank": "2",
        "send_time": str(datetime(2024, 9, 15, 9, 15)),
        "send_flag": False
    }
]

@router.get('/all', response_model=List[MailAllResponseSchema])
async def read_users():
    return fake_mails

# @router.get('/test')
# async def read_users(request: Request, db: Session = Depends(get_db)):
#     access_token = request.cookies.get("access_token")
#     mail_list = login.get_all_emails(access_token)
#     print("*"*100)
#     for mail in mail_list:
#         db_mail = crud_mail.get_message_by_mail_id(db, mail_id=mail[0])
#         print(db_mail)
#         if db_mail:
            
#             print(db_mail)
#             print("*"*10)
#             return "OK"
#         else:
#             rank = get_email_importance(mail[4])
#             print("-"*100)
#             print(rank)
#             rank = str(rank)
#             mail_create = MailCreateSchema(
#                 mail_id = mail[0],
#                 user_id = "3",
#                 title = mail[1],
#                 your_name = mail[2],
#                 your_mail_address = mail[3],
#                 body = mail[4],
#                 send_time = mail[5],
#                 rank = rank,
#             )
#             created_mail = crud_mail.create_message(db, mail_create)
#             return "ODDD"



@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user():
    return {
        "mail_id": "1",
        "title": "テストメール1",
        "body": "これはテストメール1の本文です。",
        "your_name": "山田 太郎",
        "your_mail_address": "taro.yamada@example.com",
        "ai_answer": "これはAIによる回答1です。",
        "rank": "A",
        "send_time": "2024-04-27T12:34:56.789123"
    }