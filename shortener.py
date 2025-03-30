from __future__ import annotations
import validators
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from test_inventures.schemas import URLShortener, URLShortenerRequest
from test_inventures import services
from sqlalchemy.orm import Session
from typing import Annotated

api = FastAPI()
ALIAS_MAX_LENGTH = 10

@api.post("/shorten")
async def shorten_url(
    request: URLShortenerRequest, db: Annotated[Session, Depends(services.get_db)],
) -> URLShortener:
    """Shorten a given URL with an optional custom alias."""
    if not validators.url(request.url):
        services.raise_exception(detail="The provided URL is invalid.")
    if request.custom_alias:
        if (
            not validators.slug(request.custom_alias)
            or len(request.custom_alias) > ALIAS_MAX_LENGTH
        ):
            services.raise_exception(detail="The custom alias is invalid.")
        if not services.is_alias_available(db=db, alias=request.custom_alias):
            services.raise_exception(detail="You cannot use that alias.")

    return services.create_shortened_url(
        db=db, url=request.url, alias=request.custom_alias,
    )

@api.get("/stats")
async def get_url_stats(
    db: Annotated[Session, Depends(services.get_db)],
    status: str | None = None, sort_by: str | None = None,
    page: int | None = 1, size: int | None = 100,
) -> list[URLShortener]:
    """Get statistics for shortened urls."""
    return services.get_stats(
        db=db, status=status, sort_by=sort_by, page=page, size=size,
    )

@api.get("/{alias}")
async def redirect_to_url(
    alias: str, request: Request, db: Annotated[Session, Depends(services.get_db)],
) -> dict:
    """Redirect to the original URL based on the alias."""
    url = services.get_by_alias(db=db, alias=alias)
    if not url:
        services.raise_exception(detail=f"The URL {request.url} is not found", code=404)
    services.add_click(db=db, url=url)
    return RedirectResponse(url.original_url, status_code=302)
