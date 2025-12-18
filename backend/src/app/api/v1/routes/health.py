from __future__ import annotations

from fastapi import APIRouter

from app.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """
    Liveness check.

    Returns immediately if the app process is up.
    """
    return {
        "ok": True,
        "service": settings.APP_NAME,
        "env": settings.ENV,
    }


@router.get("/ready")
def ready() -> dict:
    """
    Readiness check.

    For now this is identical to /health.
    DB + external checks are added in later gates.
    """
    return {"ready": True}