# location: backend/src/app/api/v1/schemas/export_job.py
# purpose: Export job schemas (playlist, CSV, etc.)

from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class ExportJobStatus(BaseModel):
    job_id: str
    status: str
    created_at: datetime