from __future__ import annotations

from typing import Callable, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.errors import Unauthorized


class AuthContext:
    """
    Lightweight auth context attached to request.state.

    Populated later by JWT/session verification (Gate 1+).
    """
    def __init__(self, user_id: Optional[str] = None, session_id: Optional[str] = None):
        self.user_id = user_id
        self.session_id = session_id


class AuthContextMiddleware(BaseHTTPMiddleware):
    """
    Initializes an empty auth context for every request.

    Real verification happens in deps/routers later; this just
    guarantees request.state.auth always exists.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Placeholder context (filled by auth deps later)
        request.state.auth = AuthContext()

        response = await call_next(request)
        return response