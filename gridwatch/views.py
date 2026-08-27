"""Page routes."""

from __future__ import annotations

from flask import Blueprint,abort, flash, g, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .auth import admin_required, login_required
from .services import grid
from .services.appliances import parse_names

bp = Blueprint("main", __name__)


def _unseen_count() -> int:
    if g.user is None:
        return 0
    row = db.query_one(
        "SELECT COUNT(*) AS n FROM notifications WHERE user_id = ? AND seen = 0", (g.user["id"],)
    )
    return row["n"] if row else 0


@bp.app_context_processor
def _nav_context():
    return {"unseen_notifications": _unseen_count()}


@bp.route("/")
@login_required
def dashboard():
    snapshot = grid.build_snapshot(g.user)
    return render_template("dashboard.html", snapshot=snapshot, page="dashboard")


@bp.route("/health")
@login_required
def health():
    snapshot = grid.build_snapshot(g.user)
    return render_template("health.html", snapshot=snapshot, data=snapshot.as_dict(), page="health")


@bp.route("/statistics")
@login_required
def statistics():
    snapshot = grid.build_snapshot(g.user)
    series = grid.history_set(g.user, snapshot)
    return render_template(
        "statistics.html",
        snapshot=snapshot,
        data=snapshot.as_dict(),
        series=series,
        page="statistics",
    )


@bp.route("/circuits")
@login_required
def circuits():
    snapshot = grid.build_snapshot(g.user, refresh=False)
    return render_template("circuits.html", snapshot=snapshot, page="circuits")


@bp.route("/notifications")
@login_required
def notifications():
    rows = db.query(
        """
        SELECT * FROM notifications
        WHERE user_id = ?
        ORDER BY seen ASC, created_at DESC, id DESC
        LIMIT 50
        """,
        (g.user["id"],),
    )
    return render_template("notifications.html", notifications=rows, page="notifications")


@bp.post("/notifications/<int:notification_id>/toggle")
@login_required
def toggle_notification(notification_id: int):
    row = db.query_one(
        "SELECT seen FROM notifications WHERE id = ? AND user_id = ?",
        (notification_id, g.user["id"]),
    )
    if row is None:
        abort(404)
    db.execute(
        "UPDATE notifications SET seen = ? WHERE id = ? AND user_id = ?",
        (0 if row["seen"] else 1, notification_id, g.user["id"]),
    )
    return redirect(url_for("main.notifications"))


@bp.post("/notifications/read-all")
@login_required
def read_all_notifications():
    db.execute("UPDATE notifications SET seen = 1 WHERE user_id = ?", (g.user["id"],))
    flash("All notifications marked as read.", "success")
    return redirect(url_for("main.notifications"))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        action = request.form.get("action", "channel")
        if action == "channel":
            priority = ",".join(parse_names(request.form.get("priority", "")))
            db.execute(
                """
                UPDATE users
                SET channel_id = ?, status_field = ?, read_api_key = ?, write_api_key = ?, priority = ?
                WHERE id = ?
                """,
                (
                    request.form.get("channel_id", "").strip() or None,
                    max(1, min(int(request.form.get("status_field") or 6), 8)),
                    request.form.get("read_api_key", "").strip() or None,
                    request.form.get("write_api_key", "").strip() or None,
                    priority,
                    g.user["id"],
                ),
            )
            flash("Channel settings saved.", "success")
        elif action == "password":
            current = request.form.get("current_password", "")
            new = request.form.get("new_password", "")
            if not check_password_hash(g.user["password_hash"], current):
                flash("Your current password is not correct.", "error")
            elif len(new) < 8:
                flash("New passwords must be at least 8 characters.", "error")
            elif new != request.form.get("confirm_password", ""):
                flash("The two new passwords do not match.", "error")
            else:
                db.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (generate_password_hash(new), g.user["id"]),
                )
                flash("Password updated.", "success")
        return redirect(url_for("main.profile"))

    commands = db.query(
        "SELECT * FROM command_log WHERE user_id = ? ORDER BY id DESC LIMIT 10", (g.user["id"],)
    )
    return render_template("profile.html", commands=commands, page="profile")


@bp.route("/about")
def about():
    return render_template("about.html", page="about")


@bp.route("/admin")
@admin_required
def admin():
    residents = db.query("SELECT * FROM users WHERE role = 'resident' ORDER BY username")
    overview = []
    for resident in residents:
        snapshot = grid.build_snapshot(resident)
        unseen = db.query_one(
            "SELECT COUNT(*) AS n FROM notifications WHERE user_id = ? AND seen = 0",
            (resident["id"],),
        )
        overview.append(
            {"resident": resident, "snapshot": snapshot, "unseen": unseen["n"] if unseen else 0}
        )
    return render_template("admin.html", overview=overview, page="admin")
