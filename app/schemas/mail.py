from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class Mail(BaseModel):
    uuid: UUID
    title: str
    answer_flag: bool
    sent_time: datetime

    class Config:
        orm_mode = True


class MailDetail(Mail):
    body: str
    answer: Optional[str]
