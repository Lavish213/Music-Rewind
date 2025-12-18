# LOCATION: backend/src/app/domain/policies/thin_data_rules.py
# COMMENT: Data minimization / redaction rules

from __future__ import annotations


def thin_payload(
    payload: dict,
    allowed_fields: set[str],
) -> dict:
    """
    Returns payload reduced to allowed fields only.
    """
    return {k: v for k, v in payload.items() if k in allowed_fields}