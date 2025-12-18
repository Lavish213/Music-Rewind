# LOCATION: backend/src/app/integrations/youtube_api/quota.py
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class QuotaSnapshot:
    used_units: int
    remaining_units: int
    reset_epoch_sec: int




class InMemoryQuota:
    """
    Simple quota tracker (local only).

    Note: YouTube quota isn't returned via standard headers.
    This is best-effort tracking so you don't accidentally spam calls.
    """

    def __init__(self, daily_units: int = 10_000):
        self._daily_units = daily_units
        self._used_units = 0
        self._reset_epoch = _next_midnight_epoch()

    def _maybe_reset(self) -> None:
        now = int(time.time())
        if now >= self._reset_epoch:
            self._used_units = 0
            self._reset_epoch = _next_midnight_epoch()

    def charge(self, units: int) -> None:
        self._maybe_reset()
        self._used_units += max(0, int(units))

    def snapshot(self) -> QuotaSnapshot:
        self._maybe_reset()
        remaining = max(0, self._daily_units - self._used_units)
        return QuotaSnapshot(
            used_units=self._used_units,
            remaining_units=remaining,
            reset_epoch_sec=self._reset_epoch,
        )


def _next_midnight_epoch() -> int:
    # Local midnight reset (good enough for dev + local worker logic)
    now = time.time()
    lt = time.localtime(now)
    # tomorrow at 00:00
    tomorrow = time.mktime(
        (lt.tm_year, lt.tm_mon, lt.tm_mday + 1, 0, 0, 0, 0, 0, -1)
    )
    return int(tomorrow)



__all__ = ["QuotaSnapshot", "InMemoryQuota"]
