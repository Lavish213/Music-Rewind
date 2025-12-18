# LOCATION: backend/src/app/domain/services/ranking_service.py
# COMMENT: Ranking orchestration wrapper

from __future__ import annotations

from app.domain.models.candidate import Candidate
from app.domain.services.candidate_service import rank_candidates


def rank(
    candidates: list[Candidate],
) -> list[Candidate]:
    return rank_candidates(candidates)