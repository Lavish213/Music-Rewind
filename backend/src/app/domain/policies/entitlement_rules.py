# LOCATION: backend/src/app/domain/policies/entitlement_rules.py
# COMMENT: Access control & feature entitlement rules

from __future__ import annotations

from app.domain.models.entitlement import Entitlement
from app.domain.models.user import User


def has_active_entitlement(
    user: User,
    entitlements: list[Entitlement],
    code: str,
) -> bool:
    """
    Returns True if user has an active entitlement matching `code`.
    """
    for ent in entitlements:
        if ent.user_id == user.id and ent.code == code and ent.is_active:
            return True
    return False