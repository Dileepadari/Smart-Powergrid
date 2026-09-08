#!/usr/bin/env python3
"""Development entry point: ``python run.py``.

Creates the database on first run so a fresh checkout works without extra
steps. For production, serve ``gridwatch:create_app()`` behind a real WSGI
server instead.
"""

from __future__ import annotations

import os
from pathlib import Path

from gridwatch import create_app
from gridwatch.db import init_db, seed_db

app = create_app()


def ensure_database() -> None:
    database = app.config["DATABASE"]
    if database == ":memory:" or Path(database).exists():
        return
    with app.app_context():
        init_db()
        seed_db()
    app.logger.info("Created %s with demo data.", database)


if __name__ == "__main__":
    ensure_database()
    app.run(
        host=os.environ.get("GRIDWATCH_HOST", "127.0.0.1"),
        port=int(os.environ.get("GRIDWATCH_PORT", "5000")),
        debug=os.environ.get("GRIDWATCH_DEBUG", "1") == "1",
    )
