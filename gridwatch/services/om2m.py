"""OM2M (oneM2M) gateway client.

The ESP boards subscribe to content instances under
``<base>/Users/<resident>/All_status``, so pushing there actuates the hardware
directly. The gateway is optional: when it is not running the app says so and
falls back to ThingSpeak.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests
from flask import current_app

log = logging.getLogger(__name__)


@dataclass
class PushResult:
    ok: bool
    detail: str


def _headers(content_type: str) -> dict[str, str]:
    return {
        "X-M2M-Origin": current_app.config["OM2M_ORIGIN"],
        "Content-Type": content_type,
    }


def is_enabled() -> bool:
    return bool(current_app.config["OM2M_ENABLED"])


def available() -> bool:
    """Cheap reachability probe used by the status badge in the UI."""
    if not is_enabled():
        return False
    base = current_app.config["OM2M_BASE_URL"].rstrip("/")
    try:
        response = requests.get(
            base,
            headers=_headers("application/json"),
            timeout=current_app.config["OM2M_TIMEOUT"],
        )
        return response.status_code < 500
    except requests.RequestException:
        return False


def read_container(resident: str, container: str) -> str | None:
    """Content of the latest instance in a container, or ``None``."""
    if not is_enabled():
        return None
    base = current_app.config["OM2M_BASE_URL"].rstrip("/")
    url = f"{base}/Users/{resident}/{container}/la"
    try:
        response = requests.get(
            url,
            headers=_headers("application/json"),
            timeout=current_app.config["OM2M_TIMEOUT"],
        )
        response.raise_for_status()
        return response.json()["m2m:cin"]["con"]
    except (requests.RequestException, ValueError, KeyError) as exc:
        log.debug("OM2M read failed for %s: %s", url, exc)
        return None


def push_status(resident: str, value: str) -> PushResult:
    """Create a content instance carrying the packed status string."""
    if not is_enabled():
        return PushResult(False, "OM2M is disabled by configuration")
    base = current_app.config["OM2M_BASE_URL"].rstrip("/")
    url = f"{base}/Users/{resident}/All_status"
    body = {"m2m:cin": {"lbl": ["status"], "con": value}}
    try:
        response = requests.post(
            url,
            json=body,
            headers=_headers("application/json;ty=4"),
            timeout=current_app.config["OM2M_TIMEOUT"],
        )
    except requests.RequestException as exc:
        log.info("OM2M unreachable: %s", exc)
        return PushResult(False, "OM2M gateway is not reachable")
    if response.status_code in (200, 201):
        return PushResult(True, "Delivered to the OM2M gateway")
    return PushResult(False, f"OM2M refused the update (HTTP {response.status_code})")
