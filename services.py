from __future__ import annotations
from test_inventures.database import SessionLocal, engine
from fastapi import HTTPException
from test_inventures.models import Base, ShortenedURL
from typing import Generator
from datetime import datetime, UTC
from sqlalchemy.orm import Session
import string
import secrets

Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    """Get Database session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_exception(detail: str, code: int = 400) -> None:
    """Raise an HTTP exception with a given detail and status code."""
    raise HTTPException(status_code=code, detail=detail)


def create_shortened_url(db: Session, url: str, alias: str | None) -> ShortenedURL:
    """Create a shortened URL entry in the database."""
    if not alias:
        alias = generate_random_alias()
        while not is_alias_available(db=db, alias=alias):
            alias = generate_random_alias()

    url = ShortenedURL(original_url=url, alias=alias)
    db.add(url)
    db.commit()
    db.refresh(url)

    return url

def generate_random_alias(length: int = 6) -> str:
    """Generate a random alias."""
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def get_by_alias(db: Session, alias: str) -> ShortenedURL:
    """Get a shortened URL entry by its alias."""
    return (
        db.query(ShortenedURL)
        .filter(
            ShortenedURL.alias == alias,
            ShortenedURL.expires_at > datetime.now(tz=UTC),
        ).first()
    )


def is_alias_available(db: Session, alias: str) -> bool:
    """Check if an alias is available."""
    return not get_by_alias(db=db, alias=alias)


def add_click(db: Session, url: ShortenedURL) -> None:
    """Increment the click count for a shortened URL."""
    url.clicks += 1
    db.commit()
    db.refresh(url)


# TODO: Check a more scalable version than this
ORDERING_OPTIONS = {
    "-clicks": ShortenedURL.clicks.desc(),
    "clicks": ShortenedURL.clicks.asc(),
    "-original_url": ShortenedURL.original_url.desc(),
    "original_url": ShortenedURL.original_url.asc(),
    "-alias": ShortenedURL.alias.desc(),
    "alias": ShortenedURL.alias.asc(),
}

def get_stats(
    db: Session, status: str | None, sort_by: str | None,
    page: int | None, size: int | None,
) -> list:
    """Get stats for all or filtered urls."""
    query = db.query(ShortenedURL)
    if status == "ACTIVE":
        query = query.filter(ShortenedURL.expires_at > datetime.now(tz=UTC))
    elif status == "INACTIVE":
        query = query.filter(ShortenedURL.expires_at <= datetime.now(tz=UTC))

    if sort_by in ORDERING_OPTIONS:
        query = query.order_by(ORDERING_OPTIONS[sort_by])

    return query.offset((page - 1) * page).limit(size).all()
