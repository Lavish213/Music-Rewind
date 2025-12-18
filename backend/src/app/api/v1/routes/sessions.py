from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.deps import require_user
from app.middleware.auth_context import AuthContext

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/me")
def get_current_session(auth: AuthContext = Depends(require_user)) -> dict:
    """
    Return the current authenticated session context.

    Real session lookup is implemented in later gates.
    """
    return {
        "user_id": auth.user_id,
        "session_id": auth.session_id,
        "status": "active",
    }


@router.post("/end")
def end_session(auth: AuthContext = Depends(require_user)) -> dict:
    """
    End the current session.

    Actual invalidation logic is added in later gates.
    """
    return {"ended": True}