from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta

class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    alias = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=datetime.utcnow + timedelta(days=3))
    clicks = Column(Integer, default=0)
