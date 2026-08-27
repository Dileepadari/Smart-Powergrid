"""Shared fixtures. Nothing here touches the network."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from gridwatch import create_app
from gridwatch.config import TestConfig
from gridwatch.db import init_db, seed_db


@pytest.fixture
def app(monkeypatch):
    # A file on disk rather than ":memory:": each request opens its own
    # connection, and an in-memory database would be empty in all but the first.
    with tempfile.TemporaryDirectory() as directory:
        application = create_app(TestConfig)
        application.config["DATABASE"] = str(Path(directory) / "test.db")

        from gridwatch.services import thingspeak

        thingspeak.clear_cache()
        monkeypatch.setattr(thingspeak, "read_feeds", lambda *a, **k: None)
        monkeypatch.setattr(thingspeak, "latest_non_null", lambda *a, **k: None)

        with application.app_context():
            init_db()
            seed_db()

        yield application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class Auth:
        def login(self, email="Resident1@students.iiit.ac.in", password="password1"):
            return client.post("/login", data={"email": email, "password": password})

        def login_admin(self):
            return self.login("admin@students.iiit.ac.in", "admin")

        def logout(self):
            return client.post("/logout")

    return Auth()
