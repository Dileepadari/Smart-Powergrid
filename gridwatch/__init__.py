"""GridWatch: a Flask front end for the smart energy grid rig.

Create the app with :func:`create_app`; ``run.py`` and the ``flask`` CLI both
go through it.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from flask import Flask, g, render_template

from . import db, security
from .config import Config, TestConfig

__all__ = ["create_app"]


def create_app(config: type[Config] | dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    if config is None:
        config = TestConfig if os.environ.get("GRIDWATCH_TESTING") else Config
    if isinstance(config, dict):
        app.config.from_object(Config)
        app.config.update(config)
    else:
        app.config.from_object(config)

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
    )

    db.register(app)
    security.register(app)

    from . import api, auth, views

    app.before_request(auth.load_logged_in_user)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(api.bp)

    from .services.appliances import control_label, display_name

    app.jinja_env.filters["fromjson"] = lambda value: json.loads(value or "{}")
    app.jinja_env.filters["appliance"] = display_name
    app.jinja_env.globals["control_label"] = control_label

    @app.url_defaults
    def _bust_static_cache(endpoint: str, values: dict[str, Any]) -> None:
        """Stamp static URLs with the file's mtime so edits are never cached."""
        if endpoint != "static" or "filename" not in values:
            return
        asset = Path(app.static_folder or "") / values["filename"]
        try:
            values["v"] = int(asset.stat().st_mtime)
        except OSError:
            pass

    @app.context_processor
    def _template_globals():
        return {
            "user": getattr(g, "user", None),
            "poll_seconds": app.config["TELEMETRY_POLL_SECONDS"],
        }

    @app.errorhandler(404)
    def _not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def _server_error(error):
        app.logger.exception("Unhandled error: %s", error)
        return render_template("errors/500.html"), 500

    return app
