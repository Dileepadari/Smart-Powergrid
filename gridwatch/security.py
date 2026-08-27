"""A small CSRF guard.

Flask ships no CSRF protection and the app has state-changing POST routes, so
every session carries a token that forms echo back in a hidden field and fetch
calls send in the ``X-CSRF-Token`` header.
"""

from __future__ import annotations

import hmac
import secrets

from flask import Flask, current_app, jsonify, request, session

SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}
HEADER = "X-CSRF-Token"


def csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def _submitted() -> str:
    return request.headers.get(HEADER) or request.form.get("csrf_token", "")


def register(app: Flask) -> None:
    @app.before_request
    def _protect():
        if request.method in SAFE_METHODS or current_app.config.get("TESTING"):
            return None
        expected = session.get("csrf_token", "")
        if not expected or not hmac.compare_digest(expected, _submitted()):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Invalid or missing CSRF token"}), 400
            return "Invalid or missing CSRF token. Reload the page and try again.", 400
        return None

    app.jinja_env.globals["csrf_token"] = csrf_token
