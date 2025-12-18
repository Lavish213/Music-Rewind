# LOCATION: backend/src/app/domain/services/signal_service.py
# COMMENT: Signal evaluation logic

from __future__ import annotations


def should_emit_signal(
    confidence: float,
    threshold: float = 0.8,
) -> bool:
    return confidence >= threshold
