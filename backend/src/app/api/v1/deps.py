from __future__ import annotations

from typing import Optional

from fastapi import Depends, Request

from app.errors import Unauthorized
from app.middleware.auth_context import AuthContext


def get_request(request: Request) -> Request:
    """Expose the raw request object as a dependency."""
    return request


def get_auth_context(request: Request) -> AuthContext:
    """
    Return the auth context attached by middleware.

    Guaranteed to exist; may be empty if unauthenticated.
    """
    auth: Optional[AuthContext] = getattr(request.state, "auth", None)
    if auth is None:
        # This should never happen if middleware is wired correctly
        raise Unauthorized("Auth context missing")
    return auth


def require_user(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
    """
    Enforce that a user is authenticated.

    Used by routes that require login.
    """
    if not auth.user_id:
        raise Unauthorized("Authentication required")
    return auth