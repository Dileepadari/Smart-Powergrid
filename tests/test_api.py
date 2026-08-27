from gridwatch.services import om2m, thingspeak


def test_snapshot_endpoint_requires_a_session(client):
    assert client.get("/api/snapshot").status_code == 302


def test_snapshot_endpoint_returns_the_grid(client, auth):
    auth.login()
    payload = client.get("/api/snapshot").get_json()
    assert payload["ok"] is True
    assert len(payload["snapshot"]["appliances"]) == 4
    assert "unseenNotifications" in payload["snapshot"]


def test_control_endpoint_switches_an_appliance(client, auth, monkeypatch):
    monkeypatch.setattr(om2m, "push_status", lambda *a, **k: om2m.PushResult(False, "offline"))
    monkeypatch.setattr(
        thingspeak, "write_status", lambda *a, **k: thingspeak.WriteResult(True, "published")
    )
    auth.login()
    payload = client.post(
        "/api/control", json={"appliance": "Motor_1", "control": "power", "value": 1}
    ).get_json()

    assert payload["ok"] is True
    assert "published" in payload["delivered"]
    motor = next(a for a in payload["snapshot"]["appliances"] if a["name"] == "Motor_1")
    assert motor["power"] == 1
    assert motor["powerLabel"] == "On"


def test_control_endpoint_validates_its_input(client, auth):
    auth.login()
    assert client.post("/api/control", json={"appliance": "Motor_1", "control": "power", "value": "x"}).status_code == 400
    assert client.post("/api/control", json={"appliance": "Nope", "control": "power", "value": 1}).status_code == 404
    assert client.post("/api/control", json={"appliance": "Buzzer_1", "control": "speed", "value": 1}).status_code == 404


def test_history_endpoint_returns_a_series(client, auth):
    auth.login()
    payload = client.get("/api/history/Motor_1").get_json()
    assert payload["ok"] is True
    assert len(payload["series"]) > 0
    assert {"t", "v"} <= set(payload["series"][0])


def test_history_endpoint_404s_on_an_unknown_appliance(client, auth):
    auth.login()
    assert client.get("/api/history/Toaster").status_code == 404
