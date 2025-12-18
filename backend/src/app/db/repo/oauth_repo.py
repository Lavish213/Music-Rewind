# LOCATION: backend/src/app/db/oauth_repo.py
# COMMENT: OAuth state persistence (login / callback safety)

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.oauth_state import OAuthState


class OAuthRepository(BaseRepository[OAuthState]):
    def __init__(self, session: Session):
        super().__init__(session, OAuthState)

    def get_by_state(self, state: str) -> OAuthState | None:
        stmt = select(OAuthState).where(OAuthState.state == state)
        return self.session.execute(stmt).scalar_one_or_none()