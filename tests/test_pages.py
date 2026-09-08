import pytest


@pytest.mark.parametrize(
    "path,needle",
    [
        ("/", b"Appliance controls"),
        ("/health", b"Appliance health"),
        ("/statistics", b"Current draw over time"),
        ("/circuits", b"Circuit layout"),
        ("/notifications", b"Alerts from your grid"),
        ("/profile", b"Channel and appliances"),
        ("/about", b"Smart energy grid failure management"),
    ],
)
def test_every_page_renders_for_a_signed_in_resident(client, auth, path, needle):
    auth.login()
    response = client.get(path)
    assert response.status_code == 200, path
    assert needle in response.data


def test_unknown_paths_render_the_404_page(client, auth):
    auth.login()
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"Page not found" in response.data


def test_notifications_can_be_toggled(client, auth, app):
    from gridwatch import db

    auth.login()
    with app.app_context():
        row = db.query_one("SELECT id, seen FROM notifications WHERE user_id = 12234 LIMIT 1")
        notification_id, seen = row["id"], row["seen"]

    client.post(f"/notifications/{notification_id}/toggle")
    with app.app_context():
        after = db.query_one("SELECT seen FROM notifications WHERE id = ?", (notification_id,))
    assert after["seen"] != seen


def test_a_resident_cannot_toggle_another_residents_notification(client, auth, app):
    from gridwatch import db

    auth.login()
    with app.app_context():
        row = db.query_one("SELECT id FROM notifications WHERE user_id = 23345 LIMIT 1")
    response = client.post(f"/notifications/{row['id']}/toggle")
    assert response.status_code == 404


def test_mark_all_read_clears_the_badge(client, auth, app):
    from gridwatch import db

    auth.login()
    client.post("/notifications/read-all")
    with app.app_context():
        row = db.query_one("SELECT COUNT(*) AS n FROM notifications WHERE user_id = 12234 AND seen = 0")
    assert row["n"] == 0


def test_profile_saves_channel_settings(client, auth, app):
    from gridwatch import db

    auth.login()
    client.post(
        "/profile",
        data={
            "action": "channel",
            "channel_id": "999",
            "status_field": "4",
            "read_api_key": "READ",
            "write_api_key": "WRITE",
            "priority": "Motor_1, LED_1",
        },
    )
    with app.app_context():
        row = db.query_one("SELECT * FROM users WHERE id = 12234")
    assert row["channel_id"] == "999"
    assert row["status_field"] == 4
    assert row["priority"] == "Motor_1,LED_1"


def test_password_change_requires_the_current_password(client, auth, app):
    from werkzeug.security import check_password_hash

    from gridwatch import db

    auth.login()
    client.post(
        "/profile",
        data={
            "action": "password",
            "current_password": "wrong",
            "new_password": "a-new-long-password",
            "confirm_password": "a-new-long-password",
        },
    )
    with app.app_context():
        row = db.query_one("SELECT password_hash FROM users WHERE id = 12234")
    assert check_password_hash(row["password_hash"], "password1")
