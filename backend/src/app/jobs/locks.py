# LOCATION: backend/src/app/jobs/locks.py
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional


# Global in-process lock registry
# Keyed by job_id (or any string identifier)
_LOCKS: Dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


@dataclass
class JobLock:
    """
    Simple, deterministic in-process job lock.

    Guarantees:
    - One execution per job_id at a time
    - No circular imports
    - Safe to import from anywhere in jobs/
    - Context-manager compatible

    NOTE:
    This is intentionally in-memory only.
    (Future: Redis / DB / file-based locks if needed)
    """

    job_id: str
    timeout_sec: Optional[float] = None

    _lock: Optional[threading.Lock] = None
    _acquired: bool = False

    def acquire(self) -> bool:
        start = time.time()

        # Ensure lock object exists atomically
        with _LOCKS_GUARD:
            if self.job_id not in _LOCKS:
                _LOCKS[self.job_id] = threading.Lock()
            self._lock = _LOCKS[self.job_id]

        # Attempt acquisition
        while True:
            acquired = self._lock.acquire(blocking=False)
            if acquired:
                self._acquired = True
                return True

            if self.timeout_sec is not None:
                if (time.time() - start) >= self.timeout_sec:
                    return False

            time.sleep(0.01)  # small backoff

    def release(self) -> None:
        if self._lock and self._acquired:
            self._lock.release()
            self._acquired = False

    # Context manager support
    def __enter__(self) -> "JobLock":
        ok = self.acquire()
        if not ok:
            raise TimeoutError(f"Could not acquire JobLock for job_id='{self.job_id}'")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


__all__ = [
    "JobLock",
]