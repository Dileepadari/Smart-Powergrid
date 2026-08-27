"""JSON endpoints the dashboard polls and posts to."""

from __future__ import annotations

from flask import Blueprint, g, jsonify, request

from . import db
from .auth import login_required
from .services import grid

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/snapshot")
@login_required
def snapshot():
    data = grid.build_snapshot(g.user).as_dict()
    row = db.query_one(
        "SELECT COUNT(*) AS n FROM notifications WHERE user_id = ? AND seen = 0", (g.user["id"],)
    )
    data["unseenNotifications"] = row["n"] if row else 0
    return jsonify({"ok": True, "snapshot": data})


@bp.post("/control")
@login_required
def control():
    payload = request.get_json(silent=True) or {}
    appliance = str(payload.get("appliance", ""))
    control_name = str(payload.get("control", ""))
    try:
        value = int(payload.get("value"))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "value must be an integer"}), 400

    try:
        snap, delivered, refused = grid.send_command(g.user, appliance, control_name, value)
    except LookupError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 404
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    return jsonify(
        {
            "ok": True,
            "delivered": delivered,
            "refused": refused,
            "snapshot": snap.as_dict(),
        }
    )


@bp.get("/history/<appliance>")
@login_required
def history(appliance: str):
    snap = grid.build_snapshot(g.user, refresh=False)
    target = next((a for a in snap.appliances if a.name == appliance), None)
    if target is None:
        return jsonify({"ok": False, "error": "Unknown appliance"}), 404
    series = grid.history_set(g.user, snap).get(appliance, [])
    return jsonify({"ok": True, "appliance": target.as_dict(), "series": series})
