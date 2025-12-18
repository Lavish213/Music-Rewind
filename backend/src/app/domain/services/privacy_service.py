# LOCATION: backend/src/app/domain/services/privacy_service.py
# COMMENT: Privacy summary + deletion orchestration

from __future__ import annotations

from app.domain.policies.retention_rules import is_expired
from datetime import datetime


def eligible_for_deletion(
    created_at: datetime,
    retention_days: int,
) -> bool:
    return is_expired(created_at, retention_days)
