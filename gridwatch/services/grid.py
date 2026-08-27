"""Grid orchestration.

Pulls the pieces together: work out which appliances a resident owns, fill in
their state and telemetry from ThingSpeak (falling back to the local cache and
then to simulation), and send control commands back out to the hardware.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

from flask import current_app

from .. import db
from . import om2m, simulation, thingspeak
from .appliances import (
    Appliance,
    apply_control,
    decode_health,
    decode_status,
    encode_status,
    overall_health,
    parse_names,
)

POWER_THEFT_THRESHOLD_MA = 5.0


@dataclass
class Snapshot:
    """Everything the dashboard, health and statistics pages need."""

    appliances: list[Appliance] = field(default_factory=list)
    status_source: str = "cache"
    health_source: str = "none"
    readings_source: str = "none"
    channel: dict = field(default_factory=dict)
    updated_at: str | None = None
    om2m_online: bool = False

    @property
    def simulated(self) -> bool:
        return {self.health_source, self.readings_source} & {"simulated", "mixed"} != set()

    @property
    def online(self) -> bool:
        return self.status_source == "thingspeak"

    @property
    def overall_health(self) -> int | None:
        return overall_health(self.appliances)

    @property
    def total_current(self) -> float:
        total = 0.0
        for appliance in self.appliances:
            for reading in appliance.readings:
                if reading["metric"] == "current":
                    total += reading["value"]
        return round(total, 1)

    @property
    def active_count(self) -> int:
        return sum(1 for a in self.appliances if a.is_on)

    def as_dict(self) -> dict:
        return {
            "appliances": [a.as_dict() for a in self.appliances],
            "statusSource": self.status_source,
            "healthSource": self.health_source,
            "readingsSource": self.readings_source,
            "simulated": self.simulated,
            "online": self.online,
            "om2mOnline": self.om2m_online,
            "updatedAt": self.updated_at,
            "overallHealth": self.overall_health,
            "totalCurrent": self.total_current,
            "activeCount": self.active_count,
            "channelId": self.channel.get("id"),
        }


def _cached_state(user_id: int) -> dict[str, tuple[int, int, int]]:
    rows = db.query(
        "SELECT appliance, power, speed, direction FROM appliance_state WHERE user_id = ? ORDER BY position",
        (user_id,),
    )
    return {r["appliance"]: (r["power"], r["speed"], r["direction"]) for r in rows}


def _known_names(user) -> list[str]:
    rows = db.query(
        "SELECT appliance FROM appliance_state WHERE user_id = ? ORDER BY position", (user["id"],)
    )
    return [r["appliance"] for r in rows]


def _persist_state(user_id: int, appliances: list[Appliance]) -> None:
    connection = db.get_db()
    for appliance in appliances:
        connection.execute(
            """
            INSERT INTO appliance_state (user_id, appliance, position, power, speed, direction, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT (user_id, appliance) DO UPDATE SET
                position = excluded.position,
                power = excluded.power,
                speed = excluded.speed,
                direction = excluded.direction,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                appliance.name,
                appliance.position,
                appliance.power,
                appliance.speed,
                appliance.direction,
            ),
        )
    connection.commit()


def _attach_readings(snapshot: Snapshot, user, channel: dict | None, live: dict[int, str]) -> None:
    """Map ThingSpeak sensor fields onto the appliance that owns them."""
    labels = thingspeak.field_names(channel, user["status_field"])
    matched_any = False
    for number, label in labels.items():
        value = live.get(number)
        if value in (None, ""):
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        metric = "temperature" if "temp" in label.lower() else "current"
        for appliance in snapshot.appliances:
            if label.lower().startswith(appliance.name.lower()):
                appliance.readings.append(
                    {"metric": metric, "label": label, "value": numeric, "field": number}
                )
                matched_any = True
                break
    if matched_any:
        snapshot.readings_source = "thingspeak"
        return

    if current_app.config["SIMULATE_MISSING_TELEMETRY"]:
        simulate_readings(snapshot, user)


def simulate_readings(snapshot: Snapshot, user) -> None:
    """Replace every appliance's readings with values derived from its state."""
    seed = str(user["id"])
    for appliance in snapshot.appliances:
        appliance.readings = [
            {
                "metric": "current",
                "label": f"{appliance.name}_current",
                "value": simulation.current_for(appliance, seed),
                "field": None,
            }
        ]
        if appliance.kind == "motor":
            appliance.readings.append(
                {
                    "metric": "temperature",
                    "label": f"{appliance.name}_temperature",
                    "value": simulation.temperature_for(appliance, seed),
                    "field": None,
                }
            )
    snapshot.readings_source = "simulated"


def build_snapshot(user, refresh: bool = True) -> Snapshot:
    """Assemble the current picture of one resident's grid."""
    snapshot = Snapshot()
    channel_id = user["channel_id"]
    status_field = user["status_field"]

    channel: dict | None = None
    feed: dict | None = None
    if refresh and channel_id:
        channel, feed = thingspeak.latest_entry(channel_id, user["read_api_key"])
    snapshot.channel = channel or {}

    names = thingspeak.appliance_names_from_channel(channel)
    if not names:
        names = parse_names(user["priority"]) or _known_names(user)
    if not names:
        return snapshot

    status_raw = None
    if channel_id and refresh:
        status_raw = thingspeak.latest_non_null(channel_id, user["read_api_key"], status_field)
    if status_raw:
        snapshot.status_source = "thingspeak"
        triples = decode_status(status_raw, names)
    else:
        cached = _cached_state(user["id"])
        triples = [cached.get(name, (0, 0, 0)) for name in names]

    for position, name in enumerate(names):
        power, speed, direction = triples[position]
        snapshot.appliances.append(
            Appliance(name=name, position=position, power=power, speed=speed, direction=direction)
        )

    health_raw = None
    if channel_id and refresh:
        health_raw = thingspeak.latest_non_null(channel_id, user["read_api_key"], status_field + 1)
    if health_raw:
        snapshot.health_source = "thingspeak"
        for appliance, score in zip(snapshot.appliances, decode_health(health_raw, names)):
            appliance.health = score
    # The rig reports 0 for appliances whose health it has not scored, so fill
    # those in individually rather than leaving holes in the chart.
    missing = [a for a in snapshot.appliances if a.health is None]
    if missing and current_app.config["SIMULATE_MISSING_TELEMETRY"]:
        seed = str(user["id"])
        for appliance in missing:
            appliance.health = simulation.health_for(appliance, seed)
            appliance.health_simulated = True
        snapshot.health_source = "mixed" if snapshot.health_source == "thingspeak" else "simulated"

    live_fields: dict[int, str] = {}
    if feed:
        for number in range(1, status_field):
            value = feed.get(f"field{number}")
            if value not in (None, ""):
                live_fields[number] = str(value)
    _attach_readings(snapshot, user, channel, live_fields)

    snapshot.updated_at = (feed or {}).get("created_at") or datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")
    snapshot.om2m_online = om2m.available()

    _persist_state(user["id"], snapshot.appliances)
    detect_anomalies(user, snapshot)
    return snapshot


def history_set(user, snapshot: Snapshot, points: int = 24) -> dict[str, list[dict]]:
    """Recent current-draw history for every appliance, on one shared time base.

    The whole set comes from a single source. Mixing a real series for one
    appliance with a simulated series for another would put two different time
    bases on the same x axis, so the readings source decides for all of them.
    """
    if snapshot.readings_source == "thingspeak":
        real = _real_history(user, snapshot, points)
        if real:
            return real
    if current_app.config["SIMULATE_MISSING_TELEMETRY"]:
        seed = str(user["id"])
        return {
            a.name: simulation.series_for(a, points=points, seed=seed) for a in snapshot.appliances
        }
    return {a.name: [] for a in snapshot.appliances}


def _real_history(user, snapshot: Snapshot, points: int) -> dict[str, list[dict]] | None:
    """Per-appliance series read straight from the channel's feed entries."""
    payload = thingspeak.read_feeds(user["channel_id"], user["read_api_key"], results=200)
    if not payload:
        return None
    channel = payload.get("channel") or {}
    labels = thingspeak.field_names(channel, user["status_field"])

    fields: dict[str, int] = {}
    for appliance in snapshot.appliances:
        match = next(
            (
                number
                for number, label in labels.items()
                if label.lower().startswith(appliance.name.lower()) and "temp" not in label.lower()
            ),
            None,
        )
        if match is not None:
            fields[appliance.name] = match
    if not fields:
        return None

    # Keep only entries where at least one appliance reported, so the axis is
    # not padded with the long stretches where the rig was powered down.
    entries = []
    for entry in payload.get("feeds") or []:
        if any(entry.get(f"field{number}") not in (None, "") for number in fields.values()):
            entries.append(entry)
    entries = entries[-points:]
    if not entries:
        return None

    series: dict[str, list[dict]] = {}
    for appliance in snapshot.appliances:
        number = fields.get(appliance.name)
        points_out = []
        for entry in entries:
            raw = entry.get(f"field{number}") if number else None
            try:
                value = float(raw)
            except (TypeError, ValueError):
                value = None
            points_out.append({"t": entry.get("created_at"), "v": value})
        series[appliance.name] = points_out
    return series


def history(user, appliance: Appliance, points: int = 24) -> list[dict]:
    """Recent current-draw history for a single appliance."""
    snapshot = build_snapshot(user, refresh=False)
    return history_set(user, snapshot, points).get(appliance.name, [])


def _recent_notification(user_id: int, appliance: str, message: str) -> bool:
    row = db.query_one(
        """
        SELECT 1 FROM notifications
        WHERE user_id = ? AND appliance = ? AND message = ?
          AND created_at > datetime('now', '-30 minutes')
        LIMIT 1
        """,
        (user_id, appliance, message),
    )
    return row is not None


def detect_anomalies(user, snapshot: Snapshot) -> list[str]:
    """Raise notifications for the failure modes the rig is built to catch."""
    raised: list[str] = []
    for appliance in snapshot.appliances:
        current = next(
            (r["value"] for r in appliance.readings if r["metric"] == "current"), None
        )
        findings: list[tuple[str, str]] = []
        if current is not None and not appliance.power and current > POWER_THEFT_THRESHOLD_MA:
            findings.append(
                (
                    "critical",
                    f"{appliance.label} is drawing {current:g} mA while switched off. Possible power theft.",
                )
            )
        if appliance.health == 1:
            findings.append(
                ("critical", f"{appliance.label} is in poor health. Inspect the circuit.")
            )
        elif appliance.health == 2:
            findings.append(
                ("warning", f"{appliance.label} is drifting from its rated draw. Schedule a check.")
            )
        for severity, message in findings:
            if _recent_notification(user["id"], appliance.name, message):
                continue
            db.execute(
                "INSERT INTO notifications (user_id, appliance, message, severity) VALUES (?, ?, ?, ?)",
                (user["id"], appliance.name, message, severity),
            )
            raised.append(message)
    return raised


def _describe(delivered: list[str], refused: list[str]) -> str:
    """One line covering both what landed and what did not."""
    if delivered and refused:
        return f"{'; '.join(delivered)} (not delivered: {'; '.join(refused)})"
    return "; ".join(delivered or refused)


def send_command(user, appliance_name: str, control: str, value: int) -> tuple[Snapshot, list[str], list[str]]:
    """Apply one control change and push the new state to the hardware.

    Returns the updated snapshot, the transports that accepted the command, and
    the ones that did not (with a reason).
    """
    snapshot = build_snapshot(user, refresh=True)
    target = next((a for a in snapshot.appliances if a.name == appliance_name), None)
    if target is None:
        raise LookupError(f"Unknown appliance {appliance_name!r}")

    apply_control(target, control, value)
    packed = encode_status(snapshot.appliances)
    _persist_state(user["id"], snapshot.appliances)

    # Simulated readings and health are functions of the state, so they have to
    # be recomputed; real readings stay as the hardware last reported them.
    if snapshot.readings_source == "simulated":
        simulate_readings(snapshot, user)
    seed = str(user["id"])
    for appliance in snapshot.appliances:
        if appliance.health_simulated:
            appliance.health = simulation.health_for(appliance, seed)

    delivered: list[str] = []
    refused: list[str] = []

    om2m_result = om2m.push_status(user["username"], packed)
    (delivered if om2m_result.ok else refused).append(om2m_result.detail)

    ts_result = thingspeak.write_status(
        user["channel_id"], user["write_api_key"], user["status_field"], packed
    )
    (delivered if ts_result.ok else refused).append(ts_result.detail)

    db.execute(
        """
        INSERT INTO command_log (user_id, appliance, payload, transport, ok, detail)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user["id"],
            appliance_name,
            json.dumps({"control": control, "value": value, "packed": packed}),
            "om2m+thingspeak",
            1 if delivered else 0,
            _describe(delivered, refused),
        ),
    )
    return snapshot, delivered, refused
