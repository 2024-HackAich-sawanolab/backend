from datetime import datetime
from typing import List
from pydantic import BaseModel
from uuid import UUID
from .book import Book


class User(BaseModel):
    id: UUID
    user_name: str
    # created_at: datetime
    # updated_at: datetime

class UserDetail(User):
    # books: List[Book] = []
    pass


class UserCreate(BaseModel):
    user_name: str
    access_token: str
    refresh_token: str
    access_token_expiry: datetime


