# LOCATION: backend/src/app/jobs/metrics.py
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class RetryRecord:
    """
    Records a single retry attempt.
    """
    attempt: int
    error: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class JobMetrics:
    """
    Deterministic, in-memory job execution metrics.

    Guarantees:
    - No side effects on import
    - No dependency on locks / retry / runner
    - Safe to construct anywhere
    """

    job_id: str
    attempts: int = 0
    retries: List[RetryRecord] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    status: str = "pending"  # pending | success | failed

    def mark_attempt(self) -> None:
        self.attempts += 1

    def mark_retry(self, *, attempt: int, error: str) -> None:
        self.retries.append(
            RetryRecord(
                attempt=attempt,
                error=error,
            )
        )

    def mark_success(self) -> None:
        self.status = "success"
        self.finished_at = time.time()

    def mark_failure(self, error: str) -> None:
        self.status = "failed"
        self.finished_at = time.time()
        self.retries.append(
            RetryRecord(
                attempt=self.attempts,
                error=error,
            )
        )

    def snapshot(self) -> Dict[str, Any]:
        """
        Serializable snapshot for logs / debugging.
        """
        return {
            "job_id": self.job_id,
            "status": self.status,
            "attempts": self.attempts,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "retries": [
                {
                    "attempt": r.attempt,
                    "error": r.error,
                    "timestamp": r.timestamp,
                }
                for r in self.retries
            ],
        }


__all__ = [
    "JobMetrics",
    "RetryRecord",
]