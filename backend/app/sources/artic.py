"""Client for the Art Institute of Chicago public API (no key needed).

Docs: https://api.artic.edu/docs/
We use it as a source of REAL artworks with real provenance text,
so the pre-flight agent has genuine data to reason about.
"""
import httpx

from app.config import PRODUCT_NAME
from app.models import Artwork

BASE_URL = "https://api.artic.edu/api/v1"
FIELDS = "id,title,artist_display,date_display,provenance_text"
# The API asks clients to identify themselves.
HEADERS = {"AIC-User-Agent": f"{PRODUCT_NAME} (portfolio project)"}


def _to_artwork(raw: dict) -> Artwork:
    return Artwork(
        id=raw["id"],
        title=raw.get("title") or "Untitled",
        artist=raw.get("artist_display"),
        date=raw.get("date_display"),
        provenance=raw.get("provenance_text"),
    )


def search_artworks(query: str, limit: int = 5) -> list[Artwork]:
    """Find artworks by keyword, e.g. 'monet'."""
    params = {"q": query, "limit": limit, "fields": FIELDS}
    response = httpx.get(f"{BASE_URL}/artworks/search", params=params, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return [_to_artwork(item) for item in response.json()["data"]]


def get_artwork(artwork_id: int) -> Artwork:
    """Fetch one artwork by its id."""
    response = httpx.get(
        f"{BASE_URL}/artworks/{artwork_id}", params={"fields": FIELDS}, headers=HEADERS, timeout=15
    )
    response.raise_for_status()
    return _to_artwork(response.json()["data"])
