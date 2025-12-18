from __future__ import annotations

from pydantic import BaseModel


class AuthStartResponse(BaseModel):
    provider: str
    status: str
    message: str


class AuthCallbackResponse(BaseModel):
    provider: str
    status: str
    message: str