# LOCATION: backend/src/app/domain/policies/ranking_rules.py
# COMMENT: Ranking weight + scoring rules

from __future__ import annotations


def compute_rank_score(
    base_score: float,
    recency_boost: float = 0.0,
    engagement_boost: float = 0.0,
) -> float:
    """
    Combines base score with optional boosts.
    """
    return base_score + recency_boost + engagement_boost


