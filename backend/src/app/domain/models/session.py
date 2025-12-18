# LOCATION: backend/src/app/domain/models/session.py
# COMMENT: Authenticated user session

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))

    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)