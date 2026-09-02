"""SQLite access layer.

One connection per request, rows returned as ``sqlite3.Row`` so templates and
services can use attribute-style keys instead of positional indexes.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

import click
from flask import Flask, current_app, g
from werkzeug.security import generate_password_hash

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_db() -> sqlite3.Connection:
    """Return the connection bound to this request, opening it if needed."""
    if "db" not in g:
        database = current_app.config["DATABASE"]
        if database != ":memory:":
            Path(database).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exception: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
    return get_db().execute(sql, params).fetchall()


def query_one(sql: str, params: Sequence[Any] = ()) -> sqlite3.Row | None:
    return get_db().execute(sql, params).fetchone()


def execute(sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
    db = get_db()
    cursor = db.execute(sql, params)
    db.commit()
    return cursor


def init_db() -> None:
    """Drop and recreate every table."""
    get_db().executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    get_db().commit()


# The demo accounts that ship with the project. Passwords are hashed on insert;
# the plaintext lives here only so a fresh checkout has something to log in with.
# ThingSpeak keys come from the environment. Left unset, the demo users seed
# without channel access and the dashboard falls back to simulated telemetry.
DEMO_USERS: tuple[dict[str, Any], ...] = (
    {
        "id": 12234,
        "username": "Resident1",
        "email": "Resident1@students.iiit.ac.in",
        "password": "password1",
        "role": "resident",
        "channel_id": "2165368",
        "status_field": 6,
        "read_api_key": os.environ.get("GRIDWATCH_DEMO1_READ_KEY", ""),
        "write_api_key": os.environ.get("GRIDWATCH_DEMO1_WRITE_KEY", ""),
        "priority": "Motor_1,Motor_2,LED_1,LED2",
    },
    {
        "id": 23345,
        "username": "Resident2",
        "email": "Resident2@students.iiit.ac.in",
        "password": "password2",
        "role": "resident",
        "channel_id": "2165370",
        "status_field": 7,
        "read_api_key": os.environ.get("GRIDWATCH_DEMO2_READ_KEY", ""),
        "write_api_key": os.environ.get("GRIDWATCH_DEMO2_WRITE_KEY", ""),
        "priority": "Motor_1,Motor_2,LED_1,Buzzer_1",
    },
    {
        "id": 91507,
        "username": "admin",
        "email": "admin@students.iiit.ac.in",
        "password": "admin",
        "role": "admin",
        "channel_id": "2165368",
        "status_field": 6,
        "read_api_key": os.environ.get("GRIDWATCH_DEMO1_READ_KEY", ""),
        "write_api_key": os.environ.get("GRIDWATCH_DEMO1_WRITE_KEY", ""),
        "priority": "",
    },
)

DEMO_NOTIFICATIONS: tuple[tuple[int, str, str, str, int], ...] = (
    (12234, "Motor_1", "Motor_1 is drawing power while switched off. Possible power theft.", "critical", 0),
    (12234, "Motor_2", "Motor_2 current is above its rated draw. Lower the potentiometer resistance.", "warning", 0),
    (12234, "LED_1", "LED_1 recovered and is reporting a healthy current draw.", "info", 1),
    (23345, "Motor_1", "Motor_1 stalled: current spiked with no change in speed.", "critical", 0),
    (23345, "Buzzer_1", "Buzzer_1 has been switched on for over an hour.", "warning", 1),
    (23345, "LED_1", "Load shedding applied. LED_1 was switched off to protect the circuit.", "info", 1),
)


def seed_db() -> None:
    """Insert the demo residents, their appliances and a few notifications."""
    db = get_db()
    for user in DEMO_USERS:
        db.execute(
            """
            INSERT INTO users (id, username, email, password_hash, role, channel_id,
                               status_field, read_api_key, write_api_key, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user["id"],
                user["username"],
                user["email"],
                generate_password_hash(user["password"]),
                user["role"],
                user["channel_id"],
                user["status_field"],
                user["read_api_key"],
                user["write_api_key"],
                user["priority"],
            ),
        )
        for position, appliance in enumerate(filter(None, user["priority"].split(","))):
            db.execute(
                """
                INSERT INTO appliance_state (user_id, appliance, position, power, speed, direction)
                VALUES (?, ?, ?, 0, 0, 0)
                """,
                (user["id"], appliance, position),
            )

    for user_id, appliance, message, severity, seen in DEMO_NOTIFICATIONS:
        db.execute(
            """
            INSERT INTO notifications (user_id, appliance, message, severity, seen)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, appliance, message, severity, seen),
        )
    db.commit()


@click.command("init-db")
@click.option("--seed/--no-seed", default=True, help="Insert the demo accounts.")
def init_db_command(seed: bool) -> None:
    """Recreate the database from schema.sql, wiping any existing data."""
    init_db()
    if seed:
        seed_db()
    click.echo(f"Initialised {current_app.config['DATABASE']}" + (" with demo data." if seed else "."))


def register(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
