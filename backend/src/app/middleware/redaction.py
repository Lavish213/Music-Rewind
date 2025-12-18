from __future__ import annotations

from typing import Any, Dict, Iterable

# Fields that should never appear in logs or error payloads
REDACT_KEYS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "jwt",
    "authorization",
    "client_secret",
    "private_key",
}


def _should_redact(key: str) -> bool:
    return key.lower() in REDACT_KEYS


def redact(obj: Any) -> Any:
    """
    Recursively redact sensitive fields from dict-like structures.

    Safe to call on:
    - dicts
    - lists
    - nested payloads
    - unknown objects (returned as-is)
    """
    if isinstance(obj, dict):
        return {
            k: ("***REDACTED***" if _should_redact(k) else redact(v))
            for k, v in obj.items()
        }

    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return [redact(v) for v in obj]

    return obj