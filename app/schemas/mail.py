from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class Mail(BaseModel):
    id: str
    title: str
    rank: str
    sent_time: datetime
    recipient_name: str
    recipient_mail_address: str


    class Config:
        orm_mode = True


class MailDetail(Mail):
    body: str
    answer: Optional[str]
