from datetime import datetime
from pydantic import BaseModel


class SessionAuthenticationCreate(BaseModel):
    user_id: int
    expires_at: datetime