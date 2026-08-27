"""Application configuration.

Every value can be overridden with an environment variable of the same name,
so the app runs unchanged in development and on a server.
"""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent


def _flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.environ.get("GRIDWATCH_SECRET_KEY", "dev-only-change-me")
    DATABASE = os.environ.get("GRIDWATCH_DATABASE", str(PROJECT_DIR / "instance" / "gridwatch.db"))

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _flag("GRIDWATCH_SECURE_COOKIES", False)
    PERMANENT_SESSION_LIFETIME = _int("GRIDWATCH_SESSION_MINUTES", 720) * 60

    # ThingSpeak is the telemetry source of record. It is read on every
    # dashboard load and written to when a resident flips a switch.
    THINGSPEAK_BASE_URL = os.environ.get("THINGSPEAK_BASE_URL", "https://api.thingspeak.com")
    THINGSPEAK_TIMEOUT = _int("THINGSPEAK_TIMEOUT", 8)
    THINGSPEAK_WRITE_ENABLED = _flag("THINGSPEAK_WRITE_ENABLED", True)
    # ThingSpeak rejects free-tier updates that arrive less than 15s apart.
    THINGSPEAK_MIN_WRITE_INTERVAL = _int("THINGSPEAK_MIN_WRITE_INTERVAL", 15)

    # OM2M is the on-premise oneM2M gateway the ESP boards subscribe to. It is
    # optional: when it is unreachable the app still works through ThingSpeak.
    OM2M_BASE_URL = os.environ.get("OM2M_BASE_URL", "http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid")
    OM2M_ORIGIN = os.environ.get("OM2M_ORIGIN", "admin:admin")
    OM2M_TIMEOUT = _int("OM2M_TIMEOUT", 3)
    OM2M_ENABLED = _flag("OM2M_ENABLED", True)

    # When the hardware has not published recently, ThingSpeak returns null
    # readings and every chart would be blank. With this on, the app fills the
    # gaps with clearly labelled simulated readings so the UI stays legible.
    SIMULATE_MISSING_TELEMETRY = _flag("GRIDWATCH_SIMULATE", True)

    # Seconds the dashboard waits between background telemetry refreshes.
    TELEMETRY_POLL_SECONDS = _int("GRIDWATCH_POLL_SECONDS", 20)


class TestConfig(Config):
    """Configuration used by the test suite: no network, throwaway database."""

    TESTING = True
    SECRET_KEY = "test"
    DATABASE = str(PROJECT_DIR / "instance" / "test.db")
    THINGSPEAK_WRITE_ENABLED = False
    OM2M_ENABLED = False
    WTF_CSRF_ENABLED = False
