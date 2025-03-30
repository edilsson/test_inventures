from test_inventures.database import SessionLocal, engine
from fastapi import HTTPException
from test_inventures.models import Base, ShortenedURL
from typing import Generator
from datetime import datetime, UTC

Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_exception(detail: str, code: int = 400):
    """Raise an HTTP exception with a given detail and status code."""
    raise HTTPException(status_code=code, detail=detail)


def create_shortened_url(db, url: str, alias: str = None) -> ShortenedURL:
    """Create a shortened URL entry in the database."""

    if not alias:
        alias = generate_random_alias()

    url = ShortenedURL(original_url=url, alias=alias)
    db.add(url)
    db.commit()
    db.refresh(url)

    return url

def generate_random_alias() -> str:
    """Generate a random alias.

    Generate a random alias for the shortened URL
    and check if it doesn't exists on the database.
    """
    # Placeholder for random alias generation logic
    # In a real implementation, you would generate a random string here
    return "random_alias"


def get_by_alias(db, alias: str) -> ShortenedURL:
    """Get a shortened URL entry by its alias."""
    return (
        db.query(ShortenedURL)
        .filter(
            ShortenedURL.alias == alias,
            ShortenedURL.expires_at > datetime.now(tz=UTC),
        ).first()
    )


def is_alias_available(db, alias: str) -> bool:
    """Check if an alias is available."""
    return not get_by_alias(db=db, alias=alias)


def add_click(db, url: ShortenedURL) -> None:
    """Increment the click count for a shortened URL."""
    url.clicks += 1
    db.commit()
    db.refresh(url)
