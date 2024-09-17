from typing import List
from pydantic import BaseModel
from uuid import UUID
from .book import Book

class GoogleLogin(BaseModel):
    uuid: UUID
    hash_sub_token: str
    class Config:
        orm_mode = True
