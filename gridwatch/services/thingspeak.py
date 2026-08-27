"""ThingSpeak client.

The hardware publishes every reading to a ThingSpeak channel, so this is the
telemetry source of record. Reads are cached briefly because the free tier is
rate limited and the dashboard polls; writes are throttled for the same reason.

Every call returns data or ``None`` and never raises, so a flaky network
degrades the page rather than breaking it.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from typing import Any

import requests
from flask import current_app

log = logging.getLogger(__name__)

_cache: dict[str, tuple[float, Any]] = {}
_cache_lock = threading.Lock()
_last_write: dict[str, float] = {}
_write_lock = threading.Lock()

CACHE_SECONDS = 10


@dataclass
class WriteResult:
    ok: bool
    detail: str


def _cached(key: str, ttl: int = CACHE_SECONDS) -> Any | None:
    with _cache_lock:
        entry = _cache.get(key)
    if entry and time.monotonic() - entry[0] < ttl:
        return entry[1]
    return None


def _store(key: str, value: Any) -> None:
    with _cache_lock:
        _cache[key] = (time.monotonic(), value)


def clear_cache() -> None:
    with _cache_lock:
        _cache.clear()


def _get(path: str, params: dict[str, Any]) -> dict | None:
    base = current_app.config["THINGSPEAK_BASE_URL"].rstrip("/")
    url = f"{base}/{path.lstrip('/')}"
    key = f"{url}?{sorted(params.items())}"
    hit = _cached(key)
    if hit is not None:
        return hit
    try:
        response = requests.get(
            url,
            params=params,
            timeout=current_app.config["THINGSPEAK_TIMEOUT"],
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        log.warning("ThingSpeak read failed for %s: %s", url, exc)
        return None
    if not isinstance(payload, dict):
        return None
    _store(key, payload)
    return payload


def read_feeds(channel_id: str, read_key: str | None, results: int = 1) -> dict | None:
    """Latest ``results`` entries for every field on a channel."""
    if not channel_id:
        return None
    params: dict[str, Any] = {"results": max(1, min(results, 8000))}
    if read_key:
        params["api_key"] = read_key
    return _get(f"channels/{channel_id}/feeds.json", params)


def latest_entry(channel_id: str, read_key: str | None) -> tuple[dict, dict] | tuple[None, None]:
    """``(channel_metadata, most_recent_feed)`` or ``(None, None)``."""
    payload = read_feeds(channel_id, read_key, results=1)
    if not payload:
        return None, None
    feeds = payload.get("feeds") or []
    return payload.get("channel") or {}, (feeds[-1] if feeds else {})


def latest_non_null(channel_id: str, read_key: str | None, field: int, lookback: int = 100) -> str | None:
    """Most recent non-null value of one field.

    The boards go quiet between demos and ThingSpeak keeps returning nulls for
    the newest entries, so the last populated value is what the UI wants.
    """
    payload = read_feeds(channel_id, read_key, results=lookback)
    if not payload:
        return None
    key = f"field{field}"
    for feed in reversed(payload.get("feeds") or []):
        value = feed.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def field_names(channel: dict | None, status_field: int) -> dict[int, str]:
    """Sensor field number -> label, for fields before the status field."""
    names: dict[int, str] = {}
    for number in range(1, max(1, status_field)):
        label = (channel or {}).get(f"field{number}")
        if label:
            names[number] = str(label)
    return names


def appliance_names_from_channel(channel: dict | None) -> list[str]:
    """The channel description doubles as the appliance list."""
    from .appliances import parse_names

    return parse_names((channel or {}).get("description"))


def write_status(channel_id: str, write_key: str | None, field: int, value: str) -> WriteResult:
    """Publish a packed status string, honouring the free-tier write interval."""
    if not current_app.config["THINGSPEAK_WRITE_ENABLED"]:
        return WriteResult(False, "ThingSpeak writes are disabled by configuration")
    if not (channel_id and write_key):
        return WriteResult(False, "No ThingSpeak write key configured for this account")

    interval = current_app.config["THINGSPEAK_MIN_WRITE_INTERVAL"]
    with _write_lock:
        previous = _last_write.get(write_key, 0.0)
        waited = time.monotonic() - previous
        if waited < interval:
            return WriteResult(False, f"ThingSpeak accepts one update every {interval}s, {int(interval - waited)}s to go")
        _last_write[write_key] = time.monotonic()

    base = current_app.config["THINGSPEAK_BASE_URL"].rstrip("/")
    try:
        response = requests.post(
            f"{base}/update.json",
            data={"api_key": write_key, f"field{field}": value},
            timeout=current_app.config["THINGSPEAK_TIMEOUT"],
        )
        response.raise_for_status()
        body = response.text.strip()
    except requests.RequestException as exc:
        log.warning("ThingSpeak write failed: %s", exc)
        with _write_lock:
            _last_write.pop(write_key, None)
        return WriteResult(False, f"ThingSpeak unreachable: {exc.__class__.__name__}")

    # A rejected update answers with entry id 0.
    entry_id = 0
    try:
        entry_id = int((response.json() or {}).get("entry_id") or 0)
    except (ValueError, AttributeError):
        entry_id = int(body) if body.isdigit() else 0
    if entry_id <= 0:
        return WriteResult(False, "ThingSpeak rejected the update")
    clear_cache()
    return WriteResult(True, f"Published to ThingSpeak as entry {entry_id}")
