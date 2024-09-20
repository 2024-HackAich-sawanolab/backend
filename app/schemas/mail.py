from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class Mail(BaseModel):
    mail_id: str
    user_id: str
    

    class Config:
        orm_mode = True

class MailCreate(Mail):
    title: Optional[str] = None
    body: Optional[str] = None
    your_name: Optional[str] = None
    your_mail_address: Optional[str] = None
    ai_answer: Optional[str] = None
    answer: Optional[str] = None
    rank: Optional[str] = None
    send_time: Optional[str] = None
    send_flag: Optional[str] = None

class MailDetail(Mail):
    body: str
    answer: Optional[str]
