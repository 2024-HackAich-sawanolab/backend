from urllib.parse import urlencode
from sqlalchemy.orm import Session
from models import SessionAuthentications
from schemas import session_authentication as sessionAuthenticationSchemas
import uuid
from models import SessionAuthentications
# from ..cruds import hash as HashCruds

def generate_session_id():
    return str(uuid.uuid4())

def store_session(db: Session, session_authentication: sessionAuthenticationSchemas.SessionAuthenticationCreate):
    db_message = SessionAuthentications(
        session_authentications_id=generate_session_id(),
        user_id = session_authentication.user_id,
        expires_at =session_authentication.expires_at
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message.session_authentications_id



def get_user_id_by_session_id(db: Session, session_id: str):
    print(type(session_id), session_id)
    session_authentication = db.query(SessionAuthentications).filter(SessionAuthentications.session_authentications_id == session_id).first()
    return session_authentication.user_id

