from pydantic import BaseModel


class URLShortener(BaseModel):
    """Model for URL shortener."""

    original_url: str
    alias: str
    created_at: str
    expires_at: str
    clicks: int = 0

    class Config:
        orm_mode = True
