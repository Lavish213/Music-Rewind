# LOCATION: backend/src/app/jobs/context.py
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class JobContext:
    """
    Execution context passed to every worker.

    Guarantees:
    - Stable attributes
    - No side effects on import
    - Safe to mutate during job execution
    """

    job_id: str
    user_id: Optional[str] = None

    started_at: float = field(default_factory=time.time)
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def set_result(self, data: Dict[str, Any]) -> None:
        """
        Explicit helper to set structured result.
        """
        if not isinstance(data, dict):
            raise TypeError("JobContext result must be a dict")
        self.result = data

    def add_meta(self, key: str, value: Any) -> None:
        """
        Attach arbitrary metadata for debugging or downstream use.
        """
        self.metadata[key] = value

    def snapshot(self) -> Dict[str, Any]:
        """
        Serializable snapshot for logs / inspection.
        """
        return {
            "job_id": self.job_id,
            "user_id": self.user_id,
            "started_at": self.started_at,
            "result": self.result,
            "metadata": self.metadata,
        }


__all__ = [
    "JobContext",
]