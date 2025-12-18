# LOCATION: backend/src/app/db/base.py
# COMMENT: Shared SQLAlchemy base + common helpers for repositories

from __future__ import annotations

from typing import TypeVar, Generic, Type
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import select

T = TypeVar("T")


class Base(DeclarativeBase):
    pass


class BaseRepository(Generic[T]):
    """
    Minimal, explicit repository base.
    No magic. No auto-commits.
    """

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, obj_id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def add(self, obj: T) -> T:
        self.session.add(obj)
        return obj