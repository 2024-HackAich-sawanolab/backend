from fastapi import HTTPException
from models import User
from schemas import user as UserSchemas
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from uuid import UUID

def read_users(db: Session):
    items = db.query(User).all()
    return items


def read_user(db: Session, user_id: UUID):
    try:
        item = db.query(User).get(user_id)
    except BaseException:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found.')

    return item

def store_user(db: Session, user: UserSchemas.UserCreate):
    db_message = User(
        user_name = user.user_name,
        access_token = user.access_token,
        refresh_token = user.refresh_token,
        access_token_expiry = user.access_token_expiry
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message.id

def get_access_token_by_user_id(db: Session, user_id: int):
    user =  db.query(User).filter(User.id == user_id).first()
    return user.access_token

