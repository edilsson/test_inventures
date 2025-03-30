from pydantic import BaseModel


class URLShortener(BaseModel):
    """Model for URL shortener."""

    original_url: str
    alias: str
    created_at: str
    expires_at: str
    clicks: int = 0

    class Config:
        from_attributes = True

class URLShortenerRequest(BaseModel):
    """Model for URL shortener request."""

    url: str
    custom_alias: str = None
