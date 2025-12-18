from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/start")
def google_auth_start() -> dict:
    """
    Placeholder: start Google OAuth flow.

    Real redirect + state handling is implemented in later gates.
    """
    return {"status": "ok", "provider": "google", "message": "OAuth start stub"}


@router.get("/google/callback")
def google_auth_callback() -> dict:
    """
    Placeholder: Google OAuth callback.

    Token exchange + user/session creation comes later.
    """
    return {"status": "ok", "provider": "google", "message": "OAuth callback stub"}


@router.get("/apple/start")
def apple_auth_start() -> dict:
    """
    Placeholder: start Apple Sign-In flow.
    """
    return {"status": "ok", "provider": "apple", "message": "OAuth start stub"}


@router.post("/apple/callback")
def apple_auth_callback() -> dict:
    """
    Placeholder: Apple Sign-In callback.
    """
    return {"status": "ok", "provider": "apple", "message": "OAuth callback stub"}