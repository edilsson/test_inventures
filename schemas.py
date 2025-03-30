"""Schemas for use in requests and responses."""
from datetime import datetime

from pydantic import BaseModel


class URLShortener(BaseModel):
    """Schema for URL shortener."""

    original_url: str
    alias: str
    created_at: datetime
    expires_at: datetime
    clicks: int = 0

    class Config:
        """Configuration for URL shortener."""

        from_attributes = True

class URLShortenerRequest(BaseModel):
    """Schema for URL shortener request."""

    url: str
    custom_alias: str = None
