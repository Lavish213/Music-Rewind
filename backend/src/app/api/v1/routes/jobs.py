from __future__ import annotations

from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from app.jobs.queue import job_queue
from app.jobs.dispatcher import dispatch_next

router = APIRouter(prefix="/jobs", tags=["jobs"])


# -------------------------
# Enqueue endpoints
# -------------------------

@router.post("/enrich")
def enqueue_enrich(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enqueue an enrich job.
    """
    job = job_queue.enqueue(
        name="enrich",
        payload=payload,
        user_id=payload.get("user_id"),
    )

    return {
        "ok": True,
        "job_id": f"enrich-{int(job.enqueued_at)}",
    }


@router.post("/import")
def enqueue_import(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enqueue an import job.
    """
    job = job_queue.enqueue(
        name="import",
        payload=payload,
        user_id=payload.get("user_id"),
    )

    return {
        "ok": True,
        "job_id": f"import-{int(job.enqueued_at)}",
    }


@router.post("/export")
def enqueue_export(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enqueue an export job.
    """
    job = job_queue.enqueue(
        name="export",
        payload=payload,
        user_id=payload.get("user_id"),
    )

    return {
        "ok": True,
        "job_id": f"export-{int(job.enqueued_at)}",
    }


# -------------------------
# Dispatch / worker trigger
# -------------------------

@router.post("/dispatch")
def dispatch_one() -> Dict[str, Any]:
    """
    Dispatch exactly one job from the queue.
    Intended for:
    - dev
    - cron
    - worker daemon
    """
    return dispatch_next()


# -------------------------
# Health / observability
# -------------------------

@router.get("/health")
def jobs_health() -> Dict[str, Any]:
    """
    Lightweight jobs health check.
    """
    return {
        "ok": True,
        "queue_depth": job_queue.size(),
    }


__all__ = ["router"]