# LOCATION: backend/src/app/domain/services/entitlement_service.py
# COMMENT: User entitlement resolution

from __future__ import annotations

from app.domain.models.user import User
from app.domain.models.entitlement import Entitlement
from app.domain.policies.entitlement_rules import has_active_entitlement


def user_has_entitlement(
    user: User,
    entitlements: list[Entitlement],
    code: str,
) -> bool:
    return has_active_entitlement(user, entitlements, code)