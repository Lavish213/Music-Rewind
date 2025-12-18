from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class SessionInfo(BaseModel):
    user_id: Optional[str]
    session_id: Optional[str]
    status: str


class EndSessionResponse(BaseModel):
    ended: bool