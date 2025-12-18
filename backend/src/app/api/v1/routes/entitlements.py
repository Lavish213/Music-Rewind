from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.deps import require_user
from app.middleware.auth_context import AuthContext

router = APIRouter(prefix="/entitlements", tags=["entitlements"])


@router.get("/")
def get_entitlements(auth: AuthContext = Depends(require_user)) -> dict:
    """
    Return the current user's entitlements.

    Real billing / receipt verification is implemented in later gates.
    """
    return {
        "user_id": auth.user_id,
        "entitlements": {
            "can_import": True,
            "can_export": True,
            "can_preview": True,
        },
    }


@router.get("/limits")
def get_limits(auth: AuthContext = Depends(require_user)) -> dict:
    """
    Return soft usage limits for the user.
    """
    return {
        "user_id": auth.user_id,
        "limits": {
            "max_candidates": 500,
            "max_imports": 5,
        },
    }