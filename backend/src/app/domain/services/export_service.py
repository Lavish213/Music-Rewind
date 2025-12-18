
# LOCATION: backend/src/app/domain/services/export_service.py
# COMMENT: Data export preparation logic

from __future__ import annotations

from app.domain.policies.thin_data_rules import thin_payload


def prepare_export(
    records: list[dict],
    allowed_fields: set[str],
) -> list[dict]:
    """
    Returns export-safe dataset.
    """
    return [thin_payload(r, allowed_fields) for r in records]

