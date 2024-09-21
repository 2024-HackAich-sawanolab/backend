from fastapi import HTTPException
from models import Mail
from sqlalchemy.orm import Session
from schemas import mail

def get_message_by_mail_id(db: Session, mail_id: str):
    return db.query(Mail).filter(Mail.mail_id == mail_id).first()

def create_message(db: Session, message: mail.MailCreate):
    db_message = Mail(
        mail_id = message.mail_id,
        user_id = message.user_id,
        title = message.title,
        your_name = message.your_name,
        your_mail_address =  message.your_mail_address,
        body = message.body,
        send_time = message.send_time,
        rank = message.rank,
        send_flag = False,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

def get_message_by_user_id(db: Session, user_id: str):
     skip = 0
     limit = 100
     return db.query(Mail).filter(Mail.user_id == user_id).offset(skip).limit(limit).all()
