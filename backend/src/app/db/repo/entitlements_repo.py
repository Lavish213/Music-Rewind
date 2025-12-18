# LOCATION: backend/src/app/db/entitlements_repo.py
# COMMENT: Entitlement persistence logic

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from app.domain.models.entitlement import Entitlement


class EntitlementsRepository(BaseRepository[Entitlement]):
    def __init__(self, session: Session):
        super().__init__(session, Entitlement)

    def get_active_for_user(self, user_id: int) -> list[Entitlement]:
        stmt = select(Entitlement).where(
            Entitlement.user_id == user_id,
            Entitlement.is_active.is_(True),
        )
        return list(self.session.execute(stmt).scalars())