from app.jobs.workers.enrich_worker import run_enrich
from app.jobs.context import JobContext

def main():
    ctx = JobContext(
        job_id="test-enrich-001",
        user_id="test-user",
        trace_id="trace-test",
    )

    payload = {
        "source": "youtube",
        "playlist_id": "TEST_PLAYLIST",
    }

    print(">>> ENRICH WORKER TEST START <<<")
    result = run_enrich(ctx, payload)
    print(">>> ENRICH WORKER RESULT <<<")
    print(result)
    print(">>> ENRICH WORKER TEST OK <<<")

if __name__ == "__main__":
    main()