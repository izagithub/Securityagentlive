"""API entry point.

Start it with:  uvicorn app.main:app --reload   (from the backend/ folder)
Then open http://127.0.0.1:8000/docs to try every endpoint in the browser.
"""
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.config import PRODUCT_NAME
from app.models import Artwork
from app.sources import artic

load_dotenv()  # reads keys from .env into environment variables

app = FastAPI(title=PRODUCT_NAME, version="0.1.0",
              description="AI security agent for live commerce")


@app.get("/health")
def health() -> dict:
    """Quick check that the service is running."""
    return {"status": "ok", "service": PRODUCT_NAME}


@app.get("/artworks/search", response_model=list[Artwork])
def search(q: str, limit: int = 5) -> list[Artwork]:
    """Search real artworks (Art Institute of Chicago)."""
    try:
        return artic.search_artworks(q, limit)
    except httpx.HTTPError as err:
        raise HTTPException(status_code=502, detail=f"Artwork source unavailable: {err}")


@app.get("/artworks/{artwork_id}", response_model=Artwork)
def artwork(artwork_id: int) -> Artwork:
    """Get one artwork with its provenance text."""
    try:
        return artic.get_artwork(artwork_id)
    except httpx.HTTPError as err:
        raise HTTPException(status_code=502, detail=f"Artwork source unavailable: {err}")


# Stage 1 will add:  POST /preflight  →  PreflightReport
