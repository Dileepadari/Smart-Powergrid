"""Authentication: sign in, sign up, sign out, and the login guards."""

from __future__ import annotations

import functools
import re
import secrets
from collections.abc import Callable

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_logged_in_user() -> None:
    """Populate ``g.user`` before every request."""
    user_id = session.get("user_id")
    g.user = (
        db.query_one("SELECT * FROM users WHERE id = ?", (user_id,)) if user_id is not None else None
    )


def login_required(view: Callable) -> Callable:
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view: Callable) -> Callable:
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        if g.user["role"] != "admin":
            flash("That page is for administrators.", "error")
            return redirect(url_for("main.dashboard"))
        return view(*args, **kwargs)

    return wrapped


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("main.dashboard"))

    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = db.query_one("SELECT * FROM users WHERE email = ? COLLATE NOCASE", (email,))
        if user is None or not check_password_hash(user["password_hash"], password):
            # Same message either way, so the form cannot be used to enumerate accounts.
            flash("That email and password combination is not recognised.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session.permanent = True
            target = request.args.get("next", "")
            if not target.startswith("/") or target.startswith("//"):
                target = url_for("main.dashboard")
            return redirect(target)

    return render_template("auth/login.html", email=email)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if g.user is not None:
        return redirect(url_for("main.dashboard"))

    form = {"username": "", "email": "", "channel_id": "", "read_api_key": "", "write_api_key": ""}
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        errors = []
        if len(form["username"]) < 3:
            errors.append("Pick a username of at least 3 characters.")
        if not EMAIL_RE.match(form["email"]):
            errors.append("Enter a valid email address.")
        if len(password) < 8:
            errors.append("Passwords must be at least 8 characters.")
        if password != confirm:
            errors.append("The two passwords do not match.")
        if db.query_one("SELECT 1 FROM users WHERE email = ? COLLATE NOCASE", (form["email"],)):
            errors.append("An account already exists for that email address.")
        if db.query_one("SELECT 1 FROM users WHERE username = ? COLLATE NOCASE", (form["username"],)):
            errors.append("That username is taken.")

        if errors:
            for message in errors:
                flash(message, "error")
        else:
            cursor = db.execute(
                """
                INSERT INTO users (id, username, email, password_hash, role, channel_id,
                                   status_field, read_api_key, write_api_key, priority)
                VALUES (?, ?, ?, ?, 'resident', ?, 6, ?, ?, '')
                """,
                (
                    secrets.randbelow(90000) + 10000,
                    form["username"],
                    form["email"],
                    generate_password_hash(password),
                    form["channel_id"] or None,
                    form["read_api_key"] or None,
                    form["write_api_key"] or None,
                ),
            )
            session.clear()
            session["user_id"] = cursor.lastrowid
            flash("Account created. Add your appliances from the profile page.", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("auth/signup.html", form=form)


@bp.post("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
