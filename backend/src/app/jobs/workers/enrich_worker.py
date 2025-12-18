# LOCATION: backend/src/app/jobs/workers/enrich_worker.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from app.integrations.youtube_api.client import YouTubeClient, YouTubeAPIError
from app.integrations.youtube_api.quota import InMemoryQuota

def run_enrich(context: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich job:
      - uses a YouTube access token to fetch playlists + playlist items
      - returns a normalized structure that can be persisted by your pipeline

    Expected payload keys (minimum):
      - access_token: str
      - user_id: str | int (optional but recommended)

    This worker does NOT write to DB directly (keeps it safe + testable).
    Caller decides persistence.

    Returns:
      {
        "ok": bool,
        "user_id": ...,
        "counts": {...},
        "data": {...},
        "errors": [...]
      }
    """
    access_token = payload.get("access_token")
    user_id = payload.get("user_id")

    if not access_token:
        return {
            "ok": False,
            "user_id": user_id,
            "counts": {},
            "data": {},
            "errors": ["missing access_token"],
        }

    quota = InMemoryQuota(daily_units=10_000)
    yt = YouTubeClient(access_token)

    errors: List[str] = []

    # 1) channel
    channel = {}
    try:
        quota.charge(1)  # channels.list is typically low unit cost
        channel = yt.channels_me()
    except YouTubeAPIError as e:
        errors.append(str(e))

    # 2) playlists (cap for safety during early dev)
    playlists: List[Dict[str, Any]] = []
    try:
        # playlists.list cost is low-ish; still track it
        # Cap playlists to avoid giant pulls in early dev
        cap_playlists = int(payload.get("cap_playlists", 25))
        quota.charge(1)
        for p in yt.iter_all_playlists():
            playlists.append(p)
            if len(playlists) >= cap_playlists:
                break
    except YouTubeAPIError as e:
        errors.append(str(e))

    # 3) playlist items (cap per playlist)
    playlist_items: Dict[str, List[Dict[str, Any]]] = {}
    try:
        cap_items = int(payload.get("cap_items_per_playlist", 200))
        for p in playlists:
            pid = p.get("id")
            if not pid:
                continue
            items: List[Dict[str, Any]] = []
            quota.charge(1)
            for it in yt.iter_all_playlist_items(pid):
                items.append(it)
                if len(items) >= cap_items:
                    break
            playlist_items[pid] = items
    except YouTubeAPIError as e:
        errors.append(str(e))

    # 4) collect video ids (optional enrichment)
    video_ids: List[str] = []
    for pid, items in playlist_items.items():
        for it in items:
            vid = (
                it.get("contentDetails", {}).get("videoId")
                or it.get("snippet", {}).get("resourceId", {}).get("videoId")
            )
            if vid:
                video_ids.append(vid)

    # de-dupe while preserving order
    video_ids = list(dict.fromkeys(video_ids))

    videos: List[Dict[str, Any]] = []
    try:
        cap_videos = int(payload.get("cap_videos", 500))
        if video_ids:
            quota.charge(1)
            videos = yt.videos_by_ids(video_ids[:cap_videos])
    except YouTubeAPIError as e:
        errors.append(str(e))

    snap = quota.snapshot()

    return {
        "ok": len(errors) == 0,
        "user_id": user_id,
        "counts": {
            "playlists": len(playlists),
            "playlist_items_total": sum(len(v) for v in playlist_items.values()),
            "video_ids": len(video_ids),
            "videos": len(videos),
        },
        "quota": {
            "used_units": snap.used_units,
            "remaining_units": snap.remaining_units,
            "reset_epoch_sec": snap.reset_epoch_sec,
        },
        "data": {
            "channel": channel,
            "playlists": playlists,
            "playlist_items": playlist_items,
            "videos": videos,
        },
        "errors": errors,
    }



__all__ = ["run_enrich"]