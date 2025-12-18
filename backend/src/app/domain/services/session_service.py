# LOCATION: backend/src/app/domain/services/session_service.py
# COMMENT: Session lifecycle logic

from __future__ import annotations
from datetime import datetime, timedelta


def is_session_expired(
    last_seen: datetime,
    ttl_minutes: int,
) -> bool:
    return datetime.utcnow() > last_seen + timedelta(minutes=ttl_minutes)
