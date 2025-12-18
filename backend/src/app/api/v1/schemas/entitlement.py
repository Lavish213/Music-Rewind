from __future__ import annotations

from pydantic import BaseModel
from typing import Dict


class EntitlementResponse(BaseModel):
    entitlements: Dict[str, bool]


class UsageLimits(BaseModel):
    max_candidates: int
    max_imports: int