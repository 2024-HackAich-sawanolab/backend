import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.mail import Mail as MailSchema, MailDetail as MailDetailSchema
import cruds.mail as mail_crud
router = APIRouter()


@router.get('/all', response_model=List[MailSchema])
async def read_users(db: Session = Depends(get_db)):
    return crud.read_users(db=db)

@router.get('/test')
async def read_users(request: Request):
    access_token = request.cookies.get("access_token")
    print(access_token)
    mail_crud.get_all_emails(access_token)

@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.read_user(user_id=user_id, db=db)