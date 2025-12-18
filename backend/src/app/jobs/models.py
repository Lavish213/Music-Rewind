# LOCATION: backend/src/app/jobs/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time


@dataclass
class JobResult:
    """
    Canonical job result returned by runner.
    """
    ok: bool
    job_id: str
    user_id: Optional[str]
    attempts: int
    data: Dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    finished_at: float = field(default_factory=lambda: time.time())


@dataclass
class JobExecution:
    """
    Internal execution state (non-persistent).
    """
    job_id: str
    name: str
    user_id: Optional[str]
    started_at: float = field(default_factory=lambda: time.time())
    attempts: int = 0

    def elapsed_sec(self) -> float:
        return time.time() - self.started_at


__all__ = ["JobResult", "JobExecution"]