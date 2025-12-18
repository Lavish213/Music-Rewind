from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class ImportJobStatus(BaseModel):
    job_id: str
    source: str
    status: str
    progress: Optional[int] = None  # 0–100
    message: Optional[str] = None