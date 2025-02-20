from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from database import Base

class SessionAuthentications(Base):
    __tablename__ = 'session_authentications'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    session_authentications_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    expires_at = Column(DateTime, nullable=False)
    last_accessed = Column(DateTime, nullable=False, default=datetime.now())