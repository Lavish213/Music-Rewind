# LOCATION: backend/src/app/jobs/runner.py
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from app.jobs.context import JobContext
from app.jobs.retry import RetryPolicy, run_with_retry
from app.jobs.metrics import JobMetrics
from app.jobs.locks import JobLock


WorkerFn = Callable[[JobContext, Dict[str, Any]], Dict[str, Any]]


def run_job(
    *,
    job_id: str,
    worker: WorkerFn,
    payload: Dict[str, Any],
    user_id: Optional[str] = None,
    retry_policy: Optional[RetryPolicy] = None,
) -> Dict[str, Any]:
    """
    Executes a job safely and consistently.

    Guarantees:
    - context exists
    - metrics recorded
    - retries applied
    - lock enforced
    - structured result returned
    """

    ctx = JobContext(
        job_id=job_id,
        user_id=user_id,
    )

    metrics = JobMetrics(job_id)
    retry_policy = retry_policy or RetryPolicy()

    def _execute() -> None:
        metrics.mark_attempt()

        result = worker(ctx, payload)

        if not isinstance(result, dict):
            raise RuntimeError("Worker must return dict result")

        ctx.result = result

    with JobLock(job_id):
        try:
            run_with_retry(
                fn=_execute,
                policy=retry_policy,
                on_error=lambda exc, state: metrics.mark_retry(
                    attempt=state.attempt,
                    error=str(exc),
                ),
            )

            metrics.mark_success()
            return {
                "ok": True,
                "job_id": job_id,
                "user_id": user_id,
                "attempts": metrics.attempts,
                "data": ctx.result or {},
                "errors": [],
            }

        except Exception as exc:
            metrics.mark_failure(str(exc))

            return {
                "ok": False,
                "job_id": job_id,
                "user_id": user_id,
                "attempts": metrics.attempts,
                "data": {},
                "errors": [str(exc)],
            }


__all__ = ["run_job"]