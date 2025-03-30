import validators
from fastapi import Depends, FastAPI, Request, Session
from test_inventures.dataclasses import URLShortener
from test_inventures import services
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

@api.get("/stats/{url}")
async def get_url_stats(url: str) -> dict:
    """Get statistics for a shortened URL."""
    # Placeholder implementation
    return {"url": url, "clicks": 42, "created_at": "2023-10-01"}

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
