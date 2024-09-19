from fastapi import HTTPException
from models import User
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from uuid import UUID
import requests


# curl -X POST "http://localhost:8889/v1/collections/my_collection/search" \
#     -H "Content-Type: application/json" \
#     -d '{"input":"ビーチで歩く"}'
def read_users(db: Session):
    items = db.query(User).all()
    requests.post('http://rag-api-1:8889/v1/collections/my_collection/search', json={'input': 'ビーチで歩く'})
    return items


def read_user(db: Session, user_id: UUID):
    try:
        item = db.query(User).get(user_id)
    except BaseException:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found.')

    return item
