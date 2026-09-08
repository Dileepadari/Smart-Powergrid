"""Snapshot assembly and the control path, with the network stubbed out."""

from gridwatch import db
from gridwatch.services import grid, om2m, thingspeak


def test_snapshot_falls_back_to_the_cached_state(app):
    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        snapshot = grid.build_snapshot(user)

    assert [a.name for a in snapshot.appliances] == ["Motor_1", "Motor_2", "LED_1", "LED2"]
    assert snapshot.status_source == "cache"
    assert snapshot.online is False


def test_snapshot_reads_live_state_when_thingspeak_answers(app, monkeypatch):
    monkeypatch.setattr(
        thingspeak,
        "latest_entry",
        lambda *a, **k: ({"id": 2165368, "description": "Motor_1,LED_1"}, {"created_at": "2026-01-01T00:00:00Z"}),
    )
    monkeypatch.setattr(
        thingspeak,
        "latest_non_null",
        lambda channel, key, field, **k: "1,2,0:0,0,0" if field == 6 else "3,1",
    )

    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        snapshot = grid.build_snapshot(user)

    assert snapshot.status_source == "thingspeak"
    assert snapshot.health_source == "thingspeak"
    assert [a.name for a in snapshot.appliances] == ["Motor_1", "LED_1"]
    motor, led = snapshot.appliances
    assert (motor.power, motor.speed, motor.direction) == (1, 2, 0)
    assert motor.health == 3
    assert led.health == 1


def test_simulation_fills_in_missing_readings(app):
    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        snapshot = grid.build_snapshot(user)

    assert snapshot.readings_source == "simulated"
    assert snapshot.simulated is True
    assert all(a.readings for a in snapshot.appliances)


def test_simulation_can_be_switched_off(app):
    app.config["SIMULATE_MISSING_TELEMETRY"] = False
    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        snapshot = grid.build_snapshot(user)

    assert snapshot.readings_source == "none"
    assert snapshot.simulated is False


def test_send_command_persists_state_even_when_no_transport_accepts_it(app, monkeypatch):
    monkeypatch.setattr(om2m, "push_status", lambda *a, **k: om2m.PushResult(False, "offline"))
    monkeypatch.setattr(
        thingspeak, "write_status", lambda *a, **k: thingspeak.WriteResult(False, "disabled")
    )

    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        _snapshot, delivered, refused = grid.send_command(user, "Motor_1", "power", 1)
        assert delivered == []
        assert len(refused) == 2

        stored = db.query_one(
            "SELECT power FROM appliance_state WHERE user_id = 12234 AND appliance = 'Motor_1'"
        )
        assert stored["power"] == 1

        logged = db.query_one("SELECT * FROM command_log WHERE user_id = 12234 ORDER BY id DESC")
        assert logged["appliance"] == "Motor_1"
        assert logged["ok"] == 0


def test_send_command_rejects_an_unknown_appliance(app):
    import pytest

    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        with pytest.raises(LookupError):
            grid.send_command(user, "Toaster", "power", 1)


def test_power_theft_raises_a_notification(app, monkeypatch):
    monkeypatch.setattr(
        thingspeak,
        "latest_entry",
        lambda *a, **k: (
            {"id": 1, "description": "Motor_1", "field1": "Motor_1_current"},
            {"created_at": "2026-01-01T00:00:00Z", "field1": "180"},
        ),
    )
    monkeypatch.setattr(
        thingspeak, "latest_non_null", lambda channel, key, field, **k: "0,0,0" if field == 6 else None
    )

    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        grid.build_snapshot(user)
        row = db.query_one(
            "SELECT message FROM notifications WHERE user_id = 12234 ORDER BY id DESC LIMIT 1"
        )

    assert "power theft" in row["message"].lower()


def test_anomaly_notifications_are_not_duplicated(app, monkeypatch):
    monkeypatch.setattr(
        thingspeak,
        "latest_entry",
        lambda *a, **k: (
            {"id": 1, "description": "Motor_1", "field1": "Motor_1_current"},
            {"created_at": "2026-01-01T00:00:00Z", "field1": "180"},
        ),
    )
    monkeypatch.setattr(
        thingspeak, "latest_non_null", lambda channel, key, field, **k: "0,0,0" if field == 6 else None
    )

    with app.app_context():
        user = db.query_one("SELECT * FROM users WHERE id = 12234")
        grid.build_snapshot(user)
        grid.build_snapshot(user)
        # Match the generated wording only: the seed data ships a similar
        # power-theft message for this resident.
        row = db.query_one(
            "SELECT COUNT(*) AS n FROM notifications WHERE user_id = 12234 AND message LIKE '%180 mA%'"
        )

    assert row["n"] == 1
