from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import require_user
from app.middleware.auth_context import AuthContext

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/")
def list_candidates(
    auth: AuthContext = Depends(require_user),
    limit: int = Query(25, ge=1, le=100),
) -> dict:
    """
    List current candidate songs for the active session.

    Real ranking + filtering logic is implemented in later gates.
    """
    return {
        "user_id": auth.user_id,
        "limit": limit,
        "candidates": [],
    }


@router.post("/narrow")
def narrow_candidates(
    auth: AuthContext = Depends(require_user),
) -> dict:
    """
    Apply user feedback to narrow candidate set.

    Signal processing is implemented in later gates.
    """
    return {
        "user_id": auth.user_id,
        "status": "narrowing_applied",
    }