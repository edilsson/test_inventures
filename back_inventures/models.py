"""Model classes for database creation/handling."""
from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class ShortenedURL(Base):
    """Model class for shortened URLs."""

    __tablename__ = "shortened_urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    alias = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    clicks = Column(Integer, default=0)
