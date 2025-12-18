# LOCATION: backend/src/app/domain/policies/retention_rules.py
# COMMENT: Data retention timing rules

from __future__ import annotations

from datetime import datetime, timedelta


def is_expired(
    created_at: datetime,
    retention_days: int,
) -> bool:
    """
    Returns True if record is past retention window.
    """
    return datetime.utcnow() > created_at + timedelta(days=retention_days)
