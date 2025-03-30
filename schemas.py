from pydantic import BaseModel
from datetime import datetime


class URLShortener(BaseModel):
    """Model for URL shortener."""

    original_url: str
    alias: str
    created_at: datetime
    expires_at: datetime
    clicks: int = 0

    class Config:
        from_attributes = True

class URLShortenerRequest(BaseModel):
    """Model for URL shortener request."""

    url: str
    custom_alias: str = None
