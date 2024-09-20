import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.mail import Mail as MailSchema, MailDetail as MailDetailSchema, MailCreate as MailCreateSchema
import app.cruds.login as login
import cruds.mail as crud_mail
router = APIRouter()


@router.get('/all', response_model=List[MailSchema])
async def read_users(db: Session = Depends(get_db)):
    return crud.read_users(db=db)

@router.get('/test')
async def read_users(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    mail_list = login.get_all_emails(access_token)
    print("*"*100)
    for mail in mail_list:
        db_mail = crud_mail.get_message_by_mail_id(db, mail_id=mail[0])
        if db_mail:
            print(db_mail)
            print("*"*10)
            return "OK"
        else:
            mail_create = MailCreateSchema(
                mail_id = mail[0],
                user_id = "3",
                title = mail[1],
                your_name = mail[2],
                your_mail_address = mail[3],
                body = mail[4],
                send_time = mail[5]
            )
            created_mail = crud_mail.create_message(db, mail_create)
            return "ODDD"



@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.read_user(user_id=user_id, db=db)