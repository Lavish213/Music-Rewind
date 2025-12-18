# LOCATION: backend/src/app/db/sessions_repo.py
# COMMENT: User session persistence

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.session import SessionModel


class SessionsRepository(BaseRepository[SessionModel]):
    def __init__(self, session: Session):
        super().__init__(session, SessionModel)

    def get_active_for_user(self, user_id: int) -> SessionModel | None:
        stmt = select(SessionModel).where(
            SessionModel.user_id == user_id,
            SessionModel.revoked.is_(False),
        )
        return self.session.execute(stmt).scalar_one_or_none()