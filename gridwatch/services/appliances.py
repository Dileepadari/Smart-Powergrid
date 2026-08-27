"""Appliance domain model.

The grid packs the state of every appliance a resident owns into a single
ThingSpeak field. One appliance is ``power,speed,direction``; appliances are
joined with colons, in the order the resident's appliance list declares:

    "1,2,0:1,0,1:0,1,1:1,1,0"

Everything that needs to read or write that string goes through this module so
the encoding is defined in exactly one place.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

POWER_LABELS = {0: "Off", 1: "On"}
SPEED_LABELS = {0: "Low", 1: "Medium", 2: "High"}
DIRECTION_LABELS = {0: "Clockwise", 1: "Anticlockwise"}
HEALTH_LABELS = {1: "Poor", 2: "Fair", 3: "Good"}

# Which controls each kind of appliance exposes.
KIND_CAPABILITIES = {
    "motor": ("power", "speed", "direction"),
    "led": ("power", "speed"),
    "buzzer": ("power",),
    "generic": ("power",),
}

KIND_ICONS = {
    "motor": "motor",
    "led": "bulb",
    "buzzer": "bell",
    "generic": "plug",
}

KIND_LABELS = {
    "motor": "Motor",
    "led": "LED",
    "buzzer": "Buzzer",
    "generic": "Appliance",
}


def classify(name: str) -> str:
    """Map an appliance name such as ``Motor_1`` onto a kind."""
    lowered = name.lower()
    if "motor" in lowered:
        return "motor"
    if "led" in lowered or "light" in lowered or "lamp" in lowered:
        return "led"
    if "buzzer" in lowered or "alarm" in lowered or "siren" in lowered:
        return "buzzer"
    return "generic"


def display_name(name: str) -> str:
    """``LED2`` -> ``LED 2``, ``Motor_1`` -> ``Motor 1``."""
    cleaned = name.replace("_", " ").strip()
    if " " not in cleaned:
        for index, char in enumerate(cleaned):
            if char.isdigit() and index:
                return f"{cleaned[:index]} {cleaned[index:]}"
    return cleaned


@dataclass
class Appliance:
    """One controllable appliance and everything the UI needs to render it."""

    name: str
    position: int
    power: int = 0
    speed: int = 0
    direction: int = 0
    health: int | None = None
    health_simulated: bool = False
    readings: list[dict] = field(default_factory=list)

    @property
    def kind(self) -> str:
        return classify(self.name)

    @property
    def icon(self) -> str:
        return KIND_ICONS[self.kind]

    @property
    def label(self) -> str:
        return display_name(self.name)

    @property
    def kind_label(self) -> str:
        return KIND_LABELS[self.kind]

    @property
    def capabilities(self) -> tuple[str, ...]:
        return KIND_CAPABILITIES[self.kind]

    @property
    def is_on(self) -> bool:
        return bool(self.power)

    @property
    def power_label(self) -> str:
        return POWER_LABELS.get(self.power, "Unknown")

    @property
    def speed_label(self) -> str:
        return SPEED_LABELS.get(self.speed, "Unknown")

    @property
    def direction_label(self) -> str:
        return DIRECTION_LABELS.get(self.direction, "Unknown")

    @property
    def health_label(self) -> str:
        return HEALTH_LABELS.get(self.health or 0, "Unknown")

    @property
    def health_status(self) -> str:
        """Status-palette role, so the template never picks a colour itself."""
        return {3: "good", 2: "warning", 1: "critical"}.get(self.health or 0, "unknown")

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "label": self.label,
            "position": self.position,
            "kind": self.kind,
            "kindLabel": self.kind_label,
            "icon": self.icon,
            "capabilities": list(self.capabilities),
            "power": self.power,
            "speed": self.speed,
            "direction": self.direction,
            "powerLabel": self.power_label,
            "speedLabel": self.speed_label,
            "directionLabel": self.direction_label,
            "health": self.health,
            "healthLabel": self.health_label,
            "healthStatus": self.health_status,
            "readings": self.readings,
        }


def parse_names(raw: str | None) -> list[str]:
    """Split an appliance list, tolerating the ``['a', 'b']`` OM2M spelling."""
    if not raw:
        return []
    cleaned = raw.strip().strip("[]")
    names = []
    for part in cleaned.split(","):
        part = part.strip().strip("'\"")
        if part:
            names.append(part)
    return names


def decode_status(raw: str | None, names: Sequence[str]) -> list[tuple[int, int, int]]:
    """Turn a packed status string into one ``(power, speed, direction)`` per name."""
    triples: list[tuple[int, int, int]] = []
    chunks = (raw or "").split(":") if raw else []
    for index in range(len(names)):
        values = [0, 0, 0]
        if index < len(chunks):
            for slot, token in enumerate(chunks[index].split(",")[:3]):
                try:
                    values[slot] = int(token.strip())
                except (TypeError, ValueError):
                    values[slot] = 0
        triples.append((values[0], values[1], values[2]))
    return triples


def encode_status(appliances: Iterable[Appliance]) -> str:
    """Inverse of :func:`decode_status`."""
    return ":".join(f"{a.power},{a.speed},{a.direction}" for a in appliances)


def decode_health(raw: str | None, names: Sequence[str]) -> list[int | None]:
    """Turn a packed health string (``"3,2,1"``) into one score per name."""
    tokens = [t.strip() for t in (raw or "").split(",")] if raw else []
    scores: list[int | None] = []
    for index in range(len(names)):
        score: int | None = None
        if index < len(tokens):
            try:
                candidate = int(tokens[index])
            except (TypeError, ValueError):
                candidate = 0
            if candidate in HEALTH_LABELS:
                score = candidate
        scores.append(score)
    return scores


def control_label(control: str, value: int) -> str:
    """``("speed", 2)`` -> ``"Speed set to High"``, for the command log."""
    labels = {"power": POWER_LABELS, "speed": SPEED_LABELS, "direction": DIRECTION_LABELS}
    name = {"power": "Power", "speed": "Speed", "direction": "Direction"}.get(control, control)
    return f"{name} set to {labels.get(control, {}).get(value, value)}"


def apply_control(appliance: Appliance, control: str, value: int) -> None:
    """Apply one control change, rejecting values the appliance cannot take."""
    if control not in appliance.capabilities:
        raise ValueError(f"{appliance.label} has no {control} control")
    limits = {"power": POWER_LABELS, "speed": SPEED_LABELS, "direction": DIRECTION_LABELS}
    if value not in limits[control]:
        raise ValueError(f"{value} is not a valid {control} value")
    setattr(appliance, control, value)


def overall_health(appliances: Sequence[Appliance]) -> int | None:
    """Mean health across appliances that reported one, as a percentage."""
    scores = [a.health for a in appliances if a.health]
    if not scores:
        return None
    return round(sum(scores) / (len(scores) * 3) * 100)
