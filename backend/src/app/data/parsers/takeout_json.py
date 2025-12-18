# location: backend/src/app/data/parsers/takeout_json.py
# purpose: Parse Takeout JSON into normalized TakeoutEvent rows

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import logging
import re

from app.data.parsers.takeout_common import (
    ParseReport,
    TakeoutEvent,
    TakeoutParseError,
    best_effort_datetime,
    build_event,
    compact_ws,
    safe_load_json,
)

log = logging.getLogger(__name__)


def _extract_title_artist_from_takeout_item(item: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Supports multiple Takeout shapes.

    Common patterns:
    - item["title"] = "Watched Some Song"
    - item["subtitles"] = [{"name": "Artist Name"}, ...]
    - item["details"] / item["header"]
    """
    title = item.get("title")
    if isinstance(title, dict):
        title = title.get("name") or title.get("text")
    if isinstance(title, str):
        title = compact_ws(title)

    artist = None
    subs = item.get("subtitles")
    if isinstance(subs, list) and subs:
        # subtitles often contain creator/channel/artist
        first = subs[0]
        if isinstance(first, dict):
            artist = first.get("name") or first.get("text")
        elif isinstance(first, str):
            artist = first

    if isinstance(artist, str):
        artist = compact_ws(artist)

    # fallback: sometimes "title" has "Song — Artist"
    if title and not artist:
        m = re.match(r"^(.*?)\s+[–—-]\s+(.*?)$", title)
        if m:
            t, a = m.group(1).strip(), m.group(2).strip()
            # keep both if they look real
            if t and a:
                title, artist = t, a

    return title or None, artist or None


def parse_takeout_json_file(path: Path) -> Tuple[List[TakeoutEvent], ParseReport]:
    """
    Parses a single Takeout JSON file.
    Returns: (events, report)
    """
    errors: List[str] = []
    events: List[TakeoutEvent] = []

    try:
        payload = safe_load_json(path)
    except TakeoutParseError as e:
        return [], ParseReport(source_file=str(path), count=0, errors=[str(e)])

    # Takeout may be a list, or a dict with items
    items: List[Any] = []
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        # common: {"items": [...]}
        for k in ("items", "events", "activity"):
            if isinstance(payload.get(k), list):
                items = payload[k]
                break
        if not items:
            # last resort: treat values as items if they look like dicts
            maybe = [v for v in payload.values() if isinstance(v, dict)]
            items = maybe

    if not items:
        return [], ParseReport(source_file=str(path), count=0, errors=["No parsable items found in JSON"])

    for idx, it in enumerate(items):
        if not isinstance(it, dict):
            continue

        try:
            occurred_at = best_effort_datetime(it)
            title, artist = _extract_title_artist_from_takeout_item(it)
            ev = build_event(
                source_file=path,
                source_kind="json",
                occurred_at=occurred_at,
                title=title,
                artist=artist,
                album=None,
                raw=it,
            )
            events.append(ev)
        except Exception as e:
            errors.append(f"row {idx}: {e}")

    return events, ParseReport(source_file=str(path), count=len(events), errors=errors)


def parse_takeout_json_folder(root: Path) -> Tuple[List[TakeoutEvent], List[ParseReport]]:
    """
    Parses all *.json under root, returns aggregate events + per-file reports.
    """
    reports: List[ParseReport] = []
    all_events: List[TakeoutEvent] = []

    for p in sorted(root.rglob("*.json")):
        evs, rep = parse_takeout_json_file(p)
        all_events.extend(evs)
        reports.append(rep)

    return all_events, reports