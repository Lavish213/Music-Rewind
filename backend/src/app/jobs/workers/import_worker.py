# LOCATION: backend/src/app/jobs/workers/import_worker.py
from __future__ import annotations

from typing import Any, Dict, List, Optional


def run_import(context: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Import worker (Phase 1 / V1)

    Contract:
      - MUST return dict (runner enforces this)
      - SHOULD NOT raise for user/data issues
      - MAY raise only for programmer errors (should be rare)

    Expected payload (one of these):
      A) {"takeout_path": "..."}               # server can read local file
      B) {"takeout_blob_key": "..."}           # blob_store key (future)
      C) {"takeout_raw": <dict|list|str>}      # already provided (dev/testing)

    Output:
      {"ok": bool, "counts": {...}, "data": {...}, "errors": [...]}
    """
    errors: List[str] = []
    user_id = payload.get("user_id")

    takeout_path = payload.get("takeout_path")
    takeout_blob_key = payload.get("takeout_blob_key")
    takeout_raw = payload.get("takeout_raw")

    if not (takeout_path or takeout_blob_key or takeout_raw is not None):
        return {
            "ok": False,
            "user_id": user_id,
            "counts": {},
            "data": {},
            "errors": ["missing takeout input (takeout_path | takeout_blob_key | takeout_raw)"],
        }

    # V1 strategy:
    # - Do NOT try to “be smart” and parse everything right now.
    # - Return a deterministic structure that downstream code can persist.
    # - Keep this worker safe: never crash on weird user exports.

    # Minimal canonical outputs (safe placeholders for now)
    parsed_events: List[Dict[str, Any]] = []
    source: str = "unknown"

    try:
        if takeout_path:
            source = "path"
            # V1: we don't parse on server yet without validated parser contract.
            # Keep it deterministic:
            parsed_events = []
        elif takeout_blob_key:
            source = "blob"
            parsed_events = []
        else:
            source = "raw"
            parsed_events = []  # V1: leave raw parse for next gate

    except Exception as exc:
        errors.append(f"import_worker exception: {exc}")

    return {
        "ok": len(errors) == 0,
        "user_id": user_id,
        "counts": {
            "events": len(parsed_events),
        },
        "data": {
            "source": source,
            "events": parsed_events,
        },
        "errors": errors,
    }


__all__ = ["run_import"]