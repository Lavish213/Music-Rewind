# LOCATION: backend/src/app/api/v1/routes/exports.py
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.jobs.queue import job_queue
from app.jobs.dispatcher import dispatch_next

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("/start")
def start_export(payload: Dict[str, Any] = Body(default_factory=dict)) -> Dict[str, Any]:
    """
    V1: enqueue export job then dispatch immediately.
    """
    user_id = payload.get("user_id")

    job_queue.enqueue(
        name="export",
        payload=payload,
        user_id=str(user_id) if user_id is not None else None,
    )

    result = dispatch_next()
    return {"ok": True, "job": {"name": "export"}, "result": result}