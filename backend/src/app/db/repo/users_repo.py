# LOCATION: backend/src/app/db/users_repo.py
# COMMENT: User persistence logic

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.candidate import Candidate


class UsersRepository(BaseRepository[Candidate]):
    def __init__(self, session: Session):
        super().__init__(session, Candidate)

    def get_by_provider_id(self, provider: str, provider_id: str) -> Candidate | None:
        stmt = select(Candidate).where(
            Candidate.oauth_provider == provider,
            Candidate.oauth_provider_id == provider_id,
        )
        return self.session.execute(stmt).scalar_one_or_none()