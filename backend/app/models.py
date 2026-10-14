"""Data shapes shared across the project.

Pydantic models validate data coming in and going out of the API,
so the agent always works with predictable fields.
"""
from typing import Literal

from pydantic import BaseModel


class Artwork(BaseModel):
    id: int
    title: str
    artist: str | None = None
    date: str | None = None
    provenance: str | None = None  # ownership history as free text
    source: str = "artic"           # where the record came from


class Finding(BaseModel):
    """One thing the agent noticed during a check."""
    check: str                                   # e.g. "provenance_gap"
    severity: Literal["info", "low", "medium", "high"]
    message: str                                 # human-readable explanation


class PreflightReport(BaseModel):
    """Stage 1 output: may this drop go live?"""
    artwork_id: int
    go_live: bool
    score: int                                   # 0–100 trust score
    findings: list[Finding]
