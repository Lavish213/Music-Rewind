# LOCATION: backend/src/app/db/candidates_repo.py
# COMMENT: Candidate persistence logic

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.candidate import Candidate


class CandidatesRepository(BaseRepository[Candidate]):
    def __init__(self, session: Session):
        super().__init__(session, Candidate)

    def get_by_email(self, email: str) -> Candidate | None:
        stmt = select(Candidate).where(Candidate.email == email)
        return self.session.execute(stmt).scalar_one_or_none()