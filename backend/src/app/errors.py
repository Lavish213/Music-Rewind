from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class AppError(HTTPException):
    """
    Base application error.

    All custom errors should extend this so we have:
    - consistent shape
    - predictable status codes
    - clean client responses
    """

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload: Dict[str, Any] = {
            "error": {
                "code": code,
                "message": message,
            }
        }
        if details:
            payload["error"]["details"] = details

        super().__init__(status_code=status_code, detail=payload)


# ---- Common errors -------------------------------------------------


class BadRequest(AppError):
    def __init__(self, message: str = "Bad request", **kwargs: Any) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="bad_request",
            message=message,
            details=kwargs or None,
        )


class Unauthorized(AppError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="unauthorized",
            message=message,
        )


class Forbidden(AppError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="forbidden",
            message=message,
        )


class NotFound(AppError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="not_found",
            message=message,
        )


class Conflict(AppError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="conflict",
            message=message,
        )


class RateLimited(AppError):
    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="rate_limited",
            message=message,
        )


class InternalError(AppError):
    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="internal_error",
            message=message,
        )