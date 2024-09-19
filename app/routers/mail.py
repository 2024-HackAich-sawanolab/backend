import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.mail import Mail as MailSchema, MailDetail as MailDetailSchema

router = APIRouter()


@router.get('/all', response_model=List[MailSchema])
async def read_users(db: Session = Depends(get_db)):
    return crud.read_users(db=db)

@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.read_user(user_id=user_id, db=db)