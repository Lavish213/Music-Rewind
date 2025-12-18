# LOCATION: backend/src/app/jobs/queue.py
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Job:
    """
    Immutable job definition.
    """
    name: str
    payload: Dict[str, Any]
    user_id: Optional[str] = None
    enqueued_at: float = field(default_factory=time.time)


class InMemoryJobQueue:
    """
    Thread-safe FIFO in-memory job queue.
    """

    def __init__(self) -> None:
        self._queue: List[Job] = []
        self._lock = threading.Lock()

    def enqueue(
        self,
        *,
        name: str,
        payload: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> Job:
        job = Job(
            name=name,
            payload=payload,
            user_id=user_id,
        )
        with self._lock:
            self._queue.append(job)
        return job

    def dequeue(self) -> Optional[Job]:
        with self._lock:
            if not self._queue:
                return None
            return self._queue.pop(0)

    def size(self) -> int:
        with self._lock:
            return len(self._queue)

    def snapshot(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {
                    "name": job.name,
                    "user_id": job.user_id,
                    "enqueued_at": job.enqueued_at,
                }
                for job in self._queue
            ]


# Global singleton queue
job_queue = InMemoryJobQueue()

__all__ = [
    "Job",
    "InMemoryJobQueue",
    "job_queue",
]