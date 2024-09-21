import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from schemas.mail import MailAllResponse as MailAllResponseSchema, MailDetail as MailDetailSchema, MailCreate as MailCreateSchema
import cruds.mail as crud_mail
import cruds.mail_send_flag as crud_send_flag
router = APIRouter()

@router.get('/all', response_model=List[MailAllResponseSchema])
async def get_message_by_user_id(db: Session = Depends(get_db), user_id="3"):
    return crud_mail.get_message_by_user_id(db=db, user_id=user_id)

@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(mail_id: str, db: Session = Depends(get_db)):
    return crud_mail.get_message_by_mail_id(db=db, mail_id=mail_id)


@router.get('/{mail_id}/send_flag')
async def store_send_flag_by_mail_id(mail_id: str, db: Session = Depends(get_db)):
    return crud_mail.store_send_flag_by_mail_id(db=db, mail_id=mail_id)

@router.get('/new_mail')
async def get_new_mai_by_mail_id(mail_id: str, db: Session = Depends(get_db)):
    return crud_mail.get_new_mai_by_mail_id(db=db, mail_id=mail_id)