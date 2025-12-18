from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.deps import require_user
from app.middleware.auth_context import AuthContext

router = APIRouter(prefix="/privacy", tags=["privacy"])


@router.get("/summary")
def privacy_summary(auth: AuthContext = Depends(require_user)) -> dict:
    """
    Return a high-level summary of what data we store and why.
    """
    return {
        "user_id": auth.user_id,
        "data_collected": [
            "authentication identifiers",
            "import metadata",
            "candidate rankings",
            "export job state",
        ],
        "data_retention": "limited and user-controlled",
    }


@router.post("/delete")
def delete_my_data(auth: AuthContext = Depends(require_user)) -> dict:
    """
    Request deletion of all user data.

    Actual deletion is queued and executed asynchronously in later gates.
    """
    return {
        "user_id": auth.user_id,
        "status": "deletion_requested",
    }