# LOCATION: backend/src/app/jobs/retry.py
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class RetryPolicy:
    """
    Defines retry behavior for a job/worker.

    Notes:
    - Deterministic backoff (no jitter) for reproducible debugging.
    - max_attempts includes the first attempt.
    """
    max_attempts: int = 3
    base_delay_sec: float = 1.0
    max_delay_sec: float = 30.0
    backoff_factor: float = 2.0

    def validate(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("RetryPolicy.max_attempts must be >= 1")
        if self.base_delay_sec < 0:
            raise ValueError("RetryPolicy.base_delay_sec must be >= 0")
        if self.max_delay_sec < 0:
            raise ValueError("RetryPolicy.max_delay_sec must be >= 0")
        if self.backoff_factor < 1:
            raise ValueError("RetryPolicy.backoff_factor must be >= 1")


@dataclass
class RetryState:
    """
    Tracks retry progress for a single run_with_retry execution.
    """
    attempt: int = 0
    last_error: Optional[str] = None

    def can_retry(self, policy: RetryPolicy) -> bool:
        # attempt is 1-based once we start
        return self.attempt < policy.max_attempts

    def next_delay(self, policy: RetryPolicy) -> float:
        # attempt 1 -> delay base*backoff^(0)
        exp = max(0, self.attempt - 1)
        delay = policy.base_delay_sec * (policy.backoff_factor ** exp)
        return min(delay, policy.max_delay_sec)


def run_with_retry(
    *,
    fn: Callable[[], None],
    policy: RetryPolicy,
    on_error: Optional[Callable[[Exception, RetryState], None]] = None,
) -> RetryState:
    """
    Executes fn with retry semantics.

    - fn: callable with no args (wrap externally as needed)
    - on_error: optional hook (metrics/logging) invoked after failure, before sleep
    - returns RetryState on success, raises the final exception on exhaustion
    """
    policy.validate()
    state = RetryState()

    while True:
        try:
            state.attempt += 1
            fn()
            return state

        except Exception as exc:
            state.last_error = str(exc)

            if on_error is not None:
                on_error(exc, state)

            if not state.can_retry(policy):
                raise

            delay = state.next_delay(policy)
            if delay > 0:
                time.sleep(delay)


__all__ = [
    "RetryPolicy",
    "RetryState",
    "run_with_retry",
]