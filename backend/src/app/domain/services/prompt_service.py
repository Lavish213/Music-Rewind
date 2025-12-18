# LOCATION: backend/src/app/domain/services/prompt_service.py
# COMMENT: Prompt shaping / safety layer

from __future__ import annotations

from app.domain.policies.thin_data_rules import thin_payload


def build_prompt_context(
    raw_context: dict,
    allowed_fields: set[str],
) -> dict:
    return thin_payload(raw_context, allowed_fields)
