from __future__ import annotations

from pydantic import BaseModel
from typing import List


class PrivacySummary(BaseModel):
    data_collected: List[str]
    data_retention: str


class DeletionRequestResponse(BaseModel):
    status: str