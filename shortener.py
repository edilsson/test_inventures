import validators
from fastapi import FastAPI, HTTPException

api = FastAPI()

@api.post("/shorten")
async def shorten_url(url: str, custom_alias: str = None) -> dict:
    """Shorten a given URL with an optional custom alias."""

    # Base validations
    if not validators.url(url):
        raise HTTPException(status_code=400, detail="The provided URL is invalid.")
    if custom_alias and not validators.slug(custom_alias):
        raise HTTPException(status_code=400, detail="The custom alias is invalid.")
    
    if custom_alias:
        return {"shortened_url": f"http://short.ly/{custom_alias}"}
    return {"shortened_url": "http://short.ly/abc123"}

@api.get("/stats/{url}")
async def get_url_stats(url: str) -> dict:
    """Get statistics for a shortened URL."""
    # Placeholder implementation
    return {"url": url, "clicks": 42, "created_at": "2023-10-01"}

@api.get("/{alias}")
async def redirect_to_url(alias: str) -> dict:
    """Redirect to the original URL based on the alias."""
    # Placeholder implementation
    return {"original_url": "http://example.com/original", "alias": alias}

