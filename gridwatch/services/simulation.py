"""Stand-in telemetry.

The demo rig is not always powered up, and ThingSpeak answers with nulls when
the boards have been quiet. Rather than show empty charts, the app fills the
gaps with plausible readings derived from the appliance's own state.

Everything produced here is flagged as simulated and the UI labels it, so a
simulated reading is never mistaken for a real one. Turn it off with
``GRIDWATCH_SIMULATE=0``.
"""

from __future__ import annotations

import hashlib
import math
from datetime import datetime, timedelta, timezone

# Nominal draw in milliamps by appliance kind and power setting.
NOMINAL_CURRENT = {
    "motor": (0.0, 210.0),
    "led": (0.0, 26.0),
    "buzzer": (0.0, 41.0),
    "generic": (0.0, 60.0),
}
SPEED_FACTOR = {0: 0.62, 1: 1.0, 2: 1.45}


def _noise(seed: str, span: float) -> float:
    """Deterministic pseudo-noise in ``[-span, span]`` from a seed string."""
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    unit = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
    return (unit * 2 - 1) * span


def current_for(appliance, seed: str = "") -> float:
    """Milliamps an appliance in this state would plausibly be drawing."""
    off, on = NOMINAL_CURRENT[appliance.kind]
    if not appliance.power:
        return round(max(0.0, off + _noise(f"{seed}{appliance.name}off", 0.8)), 1)
    base = on * SPEED_FACTOR.get(appliance.speed, 1.0)
    if appliance.kind == "motor" and appliance.direction:
        base *= 1.04  # anticlockwise runs marginally heavier on this rig
    return round(max(0.0, base + _noise(f"{seed}{appliance.name}on", base * 0.06)), 1)


def temperature_for(appliance, seed: str = "") -> float:
    """Degrees celsius, rising with load."""
    ambient = 28.0
    if not appliance.power:
        return round(ambient + _noise(f"{seed}{appliance.name}t0", 0.6), 1)
    rise = {"motor": 14.0, "led": 5.0, "buzzer": 4.0, "generic": 6.0}[appliance.kind]
    rise *= SPEED_FACTOR.get(appliance.speed, 1.0)
    return round(ambient + rise + _noise(f"{seed}{appliance.name}t1", 1.4), 1)


def health_for(appliance, seed: str = "") -> int:
    """A 1-3 health score consistent with the appliance's simulated draw."""
    if not appliance.power:
        return 3
    _off, on = NOMINAL_CURRENT[appliance.kind]
    expected = on * SPEED_FACTOR.get(appliance.speed, 1.0)
    actual = current_for(appliance, seed)
    if expected <= 0:
        return 3
    drift = abs(actual - expected) / expected
    if drift > 0.22:
        return 1
    if drift > 0.10:
        return 2
    return 3


def series_for(appliance, points: int = 24, minutes: int = 5, seed: str = "") -> list[dict]:
    """A short current-draw history ending now, for the statistics charts."""
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    base = current_for(appliance, seed)
    out = []
    for step in range(points - 1, -1, -1):
        stamp = now - timedelta(minutes=minutes * step)
        wave = math.sin(step / 3.1) * base * 0.05
        jitter = _noise(f"{seed}{appliance.name}{step}", base * 0.045)
        out.append(
            {
                "t": stamp.isoformat().replace("+00:00", "Z"),
                "v": round(max(0.0, base + wave + jitter), 1),
            }
        )
    return out
