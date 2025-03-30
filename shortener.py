import validators
from fastapi import Depends, FastAPI, Request, Session
from test_inventures.dataclasses import URLShortener
from test_inventures import services

api = FastAPI()

@api.post("/shorten", response_model=URLShortener)
async def shorten_url(
    url: str, custom_alias: str = None, db: Session = Depends(services.get_db)
    ):
    """Shorten a given URL with an optional custom alias."""
    # Base validations
    if not validators.url(url):
        services.raise_exception(detail="The provided URL is invalid.")
    if custom_alias and not validators.slug(custom_alias):
        services.raise_exception(detail="The custom alias is invalid.")
    if custom_alias and not services.is_alias_available(custom_alias):
        services.raise_exception(detail="You cannot use that alias.")

    return services.create_shortened_url(db=db, url=url, alias=custom_alias)

@api.get("/stats/{url}")
async def get_url_stats(url: str) -> dict:
    """Get statistics for a shortened URL."""
    # Placeholder implementation
    return {"url": url, "clicks": 42, "created_at": "2023-10-01"}

@api.get("/{alias}")
async def redirect_to_url(alias: str, request: Request, db: Session = Depends(services.get_db)) -> dict:
    """Redirect to the original URL based on the alias."""
    # Placeholder implementation
    url = services.get_by_alias(db=db, alias=alias)
    if not url:
        services.raise_exception(detail=f"The URL {request.url} is not found", code=404)
    services.add_click(db=db, url=url)
    return RedirectResponse(url.original_url, status_code=302)
