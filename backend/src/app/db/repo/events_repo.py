# LOCATION: backend/src/app/db/events_repo.py
# COMMENT: Event persistence logic

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.event import Event


class EventsRepository(BaseRepository[Event]):
    def __init__(self, session: Session):
        super().__init__(session, Event)

    def get_for_user(self, user_id: int) -> list[Event]:
        stmt = select(Event).where(Event.user_id == user_id)
        return list(self.session.execute(stmt).scalars())