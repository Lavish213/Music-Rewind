# LOCATION: backend/src/app/domain/models/event.py
# COMMENT: Audit / activity events

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))

    type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[str | None] = mapped_column(nullable=True)