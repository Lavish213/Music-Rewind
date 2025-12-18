# LOCATION: backend/src/app/domain/policies/preview_rules.py
# COMMENT: Preview / limited-access gating logic

from __future__ import annotations


def preview_limit_reached(
    preview_count: int,
    max_previews: int = 3,
) -> bool:
    """
    Returns True if preview limit has been exceeded.
    """
    return preview_count >= max_previews