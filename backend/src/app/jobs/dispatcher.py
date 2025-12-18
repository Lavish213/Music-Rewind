# LOCATION: backend/src/app/jobs/dispatcher.py
from __future__ import annotations

from typing import Any, Dict

from app.jobs.queue import job_queue
from app.jobs.runner import run_job
from app.jobs.workers.enrich_worker import run_enrich
from app.jobs.workers.import_worker import run_import
from app.jobs.workers.export_worker import run_export


WORKERS = {
    "enrich": run_enrich,
    "import": run_import,
    "export": run_export,
}


def dispatch_next() -> Dict[str, Any]:
    job = job_queue.dequeue()

    if not job:
        return {"ok": True, "message": "no jobs"}

    worker = WORKERS.get(job.name)
    if not worker:
        return {"ok": False, "errors": [f"Unknown job type: {job.name}"]}

    return run_job(
        job_id=f"{job.name}-{int(job.enqueued_at)}",
        worker=worker,
        payload=job.payload,
        user_id=job.user_id,
    )


__all__ = ["dispatch_next"]