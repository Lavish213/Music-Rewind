from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class Candidate(BaseModel):
    id: str
    title: str
    artist: Optional[str] = None
    year: Optional[int] = None
    confidence: Optional[float] = None


class CandidateListResponse(BaseModel):
    candidates: list[Candidate]
    limit: int