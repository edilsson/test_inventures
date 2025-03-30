"""Model classes for database creation/handling."""
from datetime import UTC, datetime, timedelta

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class ShortenedURL(Base):
    """Model class for shortened URLs."""

    __tablename__ = "shortened_urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    alias = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(tz=UTC))
    expires_at = Column(DateTime, default=datetime.now(tz=UTC) + timedelta(days=3))
    clicks = Column(Integer, default=0)
