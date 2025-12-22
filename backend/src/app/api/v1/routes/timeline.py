from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(tags=["timeline"])

TIMELINE_DATA = [
    {
        "id": "evt_001",
        "year": 2018,
        "title": "First Song Saved",
        "type": "memory",
        "created_at": "2018-06-12T00:00:00Z",
    },
    {
        "id": "evt_002",
        "year": 2020,
        "title": "Music Rewind Started",
        "type": "event",
        "created_at": "2020-01-01T00:00:00Z",
    },
]

@router.get("/timeline")
def get_timeline(year: Optional[int] = Query(None)):
    items = TIMELINE_DATA

    if year is not None:
        items = [item for item in items if item["year"] == year]

    return {
        "status": "ok",
        "items": items,
    }