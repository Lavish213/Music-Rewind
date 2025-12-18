# LOCATION: backend/src/app/domain/services/candidate_service.py
# COMMENT: Candidate aggregation + ranking orchestration

from __future__ import annotations

from app.domain.models.candidate import Candidate
from app.domain.policies.ranking_rules import compute_rank_score
from app.domain.policies.preview_rules import preview_limit_reached


def rank_candidates(
    candidates: list[Candidate],
) -> list[Candidate]:
    """
    Applies ranking score to candidates and returns sorted list.
    """
    for c in candidates:
        c.rank_score = compute_rank_score(
            base_score=c.base_score,
            recency_boost=c.recency_boost,
            engagement_boost=c.engagement_boost,
        )

    return sorted(candidates, key=lambda c: c.rank_score, reverse=True)
