# location: backend/src/app/data/parsers/takeout_html.py
# purpose: Parse Takeout HTML into normalized TakeoutEvent rows (no external deps)

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple
import logging
import re

from app.data.parsers.takeout_common import (
    ParseReport,
    TakeoutEvent,
    build_event,
    compact_ws,
    parse_iso_datetime,
    safe_read_text,
    strip_html_tags,
)

log = logging.getLogger(__name__)

# Google Takeout HTML often contains repeated "content-cell" blocks.
_BLOCK_RE = re.compile(r'(<div[^>]+class="content-cell[^"]*"[^>]*>.*?</div>)', re.DOTALL | re.IGNORECASE)
# Often timestamps appear as: <div class="content-cell ..."><a ...>Title</a><br>Jan 1, 2023, 1:23:45 PM UTC</div>
# But formats vary. We'll attempt ISO first, then fallback to "UTC" style text.
_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z")


def _extract_title_artist_from_block(text_block: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Very conservative: strip tags, then infer title/artist if possible.
    """
    plain = strip_html_tags(text_block)
    if not plain:
        return None, None

    # many blocks become: "Watched Song Title Artist Name Jan 1, 2023..."
    # We try to keep first chunk as title.
    parts = [p for p in re.split(r"\s{2,}|\n", plain) if p.strip()]
    joined = compact_ws(" ".join(parts))

    # If there's a " - " pattern, use it.
    m = re.match(r"^(.*?)[–—-]\s+(.*)$", joined)
    if m:
        return m.group(1).strip() or None, m.group(2).strip() or None

    # Else: first phrase as title, no artist
    # (routes later can improve via matching/search)
    return joined or None, None


def _extract_datetime_from_block(text_block: str) -> Optional[str]:
    """
    Returns an ISO-ish string if found (best effort).
    """
    m = _ISO_RE.search(text_block)
    if m:
        return m.group(0)

    # fallback: look for "UTC" / "GMT" lines after stripping
    plain = strip_html_tags(text_block)
    if "UTC" in plain or "GMT" in plain:
        return plain  # we will fail parsing, but keep raw; occurred_at None

    return None


def parse_takeout_html_file(path: Path) -> Tuple[List[TakeoutEvent], ParseReport]:
    errors: List[str] = []
    events: List[TakeoutEvent] = []

    html = safe_read_text(path)
    blocks = _BLOCK_RE.findall(html)
    if not blocks:
        # fallback: treat entire file as 1 block list (some takeouts don't use content-cell)
        blocks = [html]

    for idx, block in enumerate(blocks):
        try:
            dt_raw = _extract_datetime_from_block(block)
            occurred_at = parse_iso_datetime(dt_raw) if isinstance(dt_raw, str) else None

            title, artist = _extract_title_artist_from_block(block)
            ev = build_event(
                source_file=path,
                source_kind="html",
                occurred_at=occurred_at,
                title=title,
                artist=artist,
                album=None,
                raw={"block": block[:2000]},  # cap for safety
            )
            events.append(ev)
        except Exception as e:
            errors.append(f"block {idx}: {e}")

    return events, ParseReport(source_file=str(path), count=len(events), errors=errors)


def parse_takeout_html_folder(root: Path) -> Tuple[List[TakeoutEvent], List[ParseReport]]:
    reports: List[ParseReport] = []
    all_events: List[TakeoutEvent] = []

    for p in sorted(root.rglob("*.html")):
        evs, rep = parse_takeout_html_file(p)
        all_events.extend(evs)
        reports.append(rep)

    return all_events, reports