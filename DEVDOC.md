# GridWatch - Developer Documentation

Technical reference for the GridWatch codebase: architecture, auth model, data
model, API surface, telemetry sources and setup. For what the app does from a
user's point of view, see [README.md](./README.md).

## Table of contents

- [Tech stack](#tech-stack)
- [Architecture overview](#architecture-overview)
- [Telemetry sources](#telemetry-sources)
- [The packed status string](#the-packed-status-string)
- [Auth model](#auth-model)
- [API surface](#api-surface)
- [Data model](#data-model)
- [Theming](#theming)
- [Configuration](#configuration)
- [Local setup](#local-setup)
- [Tests](#tests)
- [Gotchas](#gotchas)

## Tech stack

Python 3.12 and Flask 3.1, using the application-factory pattern. SQLite through
the standard library, one connection per request, every query parameterised.
Passwords hashed with Werkzeug's `generate_password_hash`. Templates are Jinja;
the front end is hand-written CSS and vanilla JS with no build step. Chart.js
4.5 is vendored under `gridwatch/static/vendor/` rather than pulled from a CDN,
so the app works offline. `requests` talks to ThingSpeak and OM2M.

## Architecture overview

```
browser
  |  HTML pages + fetch() to /api/*
  v
Flask app  (gridwatch/)
  |  __init__.py     application factory, error handlers, Jinja filters
  |  auth.py         login / signup / logout, login_required, admin_required
  |  views.py        page routes
  |  api.py          JSON routes the dashboard polls and posts to
  |  security.py     CSRF guard on every unsafe method
  |  db.py           SQLite connection, schema, seed, `init-db` CLI command
  v
services/
  |  grid.py         orchestration: builds a Snapshot, sends commands
  |  appliances.py   domain model, status encode/decode, control validation
  |  thingspeak.py   channel reads (cached) and writes (throttled)
  |  om2m.py         oneM2M gateway push and reachability probe
  |  simulation.py   stand-in readings when the rig is quiet
  v
ThingSpeak (cloud)          OM2M gateway (localhost:5089)
```

`grid.build_snapshot(user)` is the one function every page goes through. It
decides which appliances the resident owns, fills in their state, health and
readings, writes the state back to the local cache, raises any anomaly
notifications, and returns a `Snapshot`. Templates and the JSON API render the
same object, so a page and its polling endpoint can never disagree.

## Telemetry sources

Each part of a snapshot records where it came from, and the UI shows it.

| Field | Order of preference |
|---|---|
| Appliance names | ThingSpeak channel description -> `users.priority` -> `appliance_state` rows |
| Power / speed / direction | ThingSpeak status field -> `appliance_state` cache |
| Health scores | ThingSpeak health field -> simulation, per appliance |
| Sensor readings | Latest ThingSpeak feed entry -> simulation |

`Snapshot.status_source` is `thingspeak` or `cache`. `health_source` is
`thingspeak`, `mixed`, `simulated` or `none`; `mixed` means the channel scored
some appliances and the rest were filled in. `readings_source` is `thingspeak`,
`simulated` or `none`.

Simulation is deterministic: values derive from a SHA-256 of the appliance name
and a seed, so the same state produces the same numbers and the dashboard does
not jitter between polls. Turn it off with `GRIDWATCH_SIMULATE=0`.

Reads are cached in-process for 10 seconds because the dashboard polls and the
free ThingSpeak tier is rate limited. Writes are throttled to one per
`THINGSPEAK_MIN_WRITE_INTERVAL` seconds (15 by default, the free-tier limit); a
write inside that window is refused with a message rather than silently dropped.

## The packed status string

The whole grid's state travels as one string in a single ThingSpeak field:

```
"1,2,0:1,0,1:0,1,1:1,1,0"
 |     |
 |     second appliance
 first appliance: power,speed,direction
```

Appliances are in the order the appliance list declares. Health uses the same
field-plus-one convention and is a flat comma-separated list of scores 1-3, with
`0` meaning "not scored".

`services/appliances.py` owns both encodings; nothing else parses these strings.
`tests/test_appliances.py` pins the round trip, since this is the contract with
the firmware in `hardware/`.

Field numbering: `users.status_field` is the field carrying the status string.
Health is `status_field + 1`. Sensor readings occupy fields `1 .. status_field-1`
and are matched to appliances by name prefix on the channel's field labels
(`Motor_1_current` belongs to `Motor_1`; a label containing `temp` is read as a
temperature).

## Auth model

Server-side sessions in a signed cookie (`SECRET_KEY`), `HttpOnly` and
`SameSite=Lax`, lasting `GRIDWATCH_SESSION_MINUTES` (12 hours by default).
`auth.load_logged_in_user` runs `before_request` and puts the user row on
`g.user`. `@login_required` redirects anonymous visitors to `/login?next=...`;
the `next` value is rejected unless it is a same-site path. `@admin_required`
additionally checks `users.role`.

Login failures return one message for both an unknown email and a wrong
password, so the form cannot be used to enumerate accounts.

CSRF: `security.py` registers a `before_request` hook that rejects any unsafe
method whose `csrf_token` form field or `X-CSRF-Token` header does not match the
session token. Forms include the hidden field; `GridWatch.postJSON` sends the
header, reading the token from `body[data-csrf]`. The check is skipped when
`TESTING` is set.

## API surface

| Method | Path | Who | Returns |
|---|---|---|---|
| GET | `/` | resident | Dashboard |
| GET | `/health` | resident | Health page |
| GET | `/statistics` | resident | Statistics page |
| GET | `/circuits` | resident | Circuits page |
| GET | `/notifications` | resident | Alert list |
| POST | `/notifications/<id>/toggle` | owner only | Redirect; 404 for another resident's alert |
| POST | `/notifications/read-all` | resident | Redirect |
| GET, POST | `/profile` | resident | Channel settings and password form |
| GET | `/about` | anyone | Static page |
| GET | `/admin` | admin | Every resident's snapshot |
| GET, POST | `/login`, `/signup` | anonymous | Auth forms |
| POST | `/logout` | anyone | Redirect to login |
| GET | `/api/snapshot` | resident | `{ok, snapshot}` including `unseenNotifications` |
| POST | `/api/control` | resident | `{ok, delivered[], refused[], snapshot}` |
| GET | `/api/history/<appliance>` | resident | `{ok, appliance, series}` |

`/api/control` takes `{"appliance": "Motor_1", "control": "power", "value": 1}`.
`control` must be one the appliance supports (a buzzer has no speed) and `value`
must be in range, or the call is a 400. An unknown appliance is a 404.

A command is attempted on both transports. `delivered` and `refused` each carry
human-readable reasons, and the response is still `ok: true` when both refuse:
the state is saved locally either way, and the UI says what happened. Every
attempt is written to `command_log`.

## Data model

SQLite, at `instance/gridwatch.db` by default. Schema in
`gridwatch/schema.sql`. All timestamps are UTC, written by SQLite's
`datetime('now')` and stored as `YYYY-MM-DD HH:MM:SS` text.

**users** - `id`, `username` (unique), `email` (unique), `password_hash`,
`role` (`resident` or `admin`, checked), `channel_id`, `status_field`,
`read_api_key`, `write_api_key`, `priority` (comma-separated appliance names in
load-shedding order), `created_at`.

**appliance_state** - last known state per appliance, keyed on
`(user_id, appliance)`: `position`, `power`, `speed`, `direction`, `updated_at`.
Written on every snapshot and every command, and read when ThingSpeak has
nothing to offer.

**notifications** - `user_id`, `appliance`, `message`, `severity` (`info`,
`warning`, `critical`, checked), `seen`, `created_at`.

**command_log** - audit trail: `user_id`, `appliance`, `payload` (JSON of the
control, value and resulting packed string), `transport`, `ok`, `detail`,
`created_at`.

Foreign keys cascade on delete and `PRAGMA foreign_keys` is enabled per
connection.

## Theming

Tokens are CSS custom properties in `gridwatch/static/css/app.css`. Light values
sit on bare `:root`; dark values are declared twice, under
`@media (prefers-color-scheme: dark)` guarded with
`:root:where(:not([data-theme="light"]))` and again under `:root[data-theme="dark"]`,
so an explicit choice wins in both directions. The choice is stored in
`localStorage` under `gridwatch-theme` and applied by an inline script in
`<head>` before first paint.

Charts read the same tokens through `getComputedStyle` rather than carrying
their own palette, and rebuild on the `gridwatch:themechange` event.

Categorical series colours are `--series-1` through `--series-6`, assigned in
fixed order and never cycled. Status colours (`--good`, `--warning`,
`--critical`) are reserved for condition and never used as a series colour;
every status is paired with an icon and a label so colour never carries the
meaning alone.

Icons are inline SVG from a single Jinja macro in
`templates/partials/icons.html`. They carry a base size from `svg.icon` in the
reset, which component rules override.

## Configuration

Every value in `gridwatch/config.py` reads an environment variable of the same
name.

| Variable | Default | Purpose |
|---|---|---|
| `GRIDWATCH_SECRET_KEY` | `dev-only-change-me` | Session signing key. Set this in production. |
| `GRIDWATCH_DATABASE` | `instance/gridwatch.db` | SQLite path |
| `GRIDWATCH_SECURE_COOKIES` | `0` | Set to `1` behind HTTPS |
| `GRIDWATCH_SESSION_MINUTES` | `720` | Session lifetime |
| `GRIDWATCH_SIMULATE` | `1` | Fill missing telemetry with stand-in values |
| `GRIDWATCH_POLL_SECONDS` | `20` | Dashboard background refresh interval |
| `THINGSPEAK_BASE_URL` | `https://api.thingspeak.com` | |
| `THINGSPEAK_TIMEOUT` | `8` | Seconds |
| `THINGSPEAK_WRITE_ENABLED` | `1` | Set to `0` to make the app read-only against the channel |
| `THINGSPEAK_MIN_WRITE_INTERVAL` | `15` | Free-tier write limit |
| `OM2M_BASE_URL` | `http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid` | |
| `OM2M_ORIGIN` | `admin:admin` | `X-M2M-Origin` header |
| `OM2M_TIMEOUT` | `3` | Seconds |
| `OM2M_ENABLED` | `1` | Set to `0` to skip the gateway entirely |
| `GRIDWATCH_HOST` / `GRIDWATCH_PORT` / `GRIDWATCH_DEBUG` | `127.0.0.1` / `5000` / `1` | `run.py` only |

## Local setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python run.py
```

`run.py` creates and seeds the database if it does not exist. To rebuild it:

```bash
.venv/bin/python -m flask --app gridwatch init-db          # with demo data
.venv/bin/python -m flask --app gridwatch init-db --no-seed
```

`init-db` drops every table, so it wipes existing data.

For production, serve `gridwatch:create_app()` from a real WSGI server and set
`GRIDWATCH_SECRET_KEY` and `GRIDWATCH_SECURE_COOKIES=1`. `run.py` uses the Flask
development server and is not meant for it.

## Tests

```bash
.venv/bin/python -m pytest tests -q
```

48 tests, no network access: the `app` fixture stubs `thingspeak.read_feeds` and
`thingspeak.latest_non_null`, and `TestConfig` disables ThingSpeak writes and
OM2M. Each test gets a fresh SQLite file in a temporary directory - not
`:memory:`, since every request opens its own connection and an in-memory
database would be empty in all but the first.

## Gotchas

- **Static assets are cache-busted by mtime.** An `url_defaults` hook appends
  `?v=<mtime>` to every `url_for('static', ...)`. Without it, browsers hold on
  to an edited stylesheet across a restart.
- **`send_command` recomputes derived values.** It builds a snapshot, applies the
  control, then regenerates simulated readings and simulated health, because
  those are functions of the state that just changed. Real readings are left
  alone: they are what the hardware last reported. `Appliance.health_simulated`
  tracks which scores may be regenerated so a mixed snapshot keeps its real ones.
- **Statistics use one source for the whole set.** Mixing a real series for one
  appliance with a simulated series for another would put two time bases on the
  same x axis, so `history_set` picks one source for all of them.
- **ThingSpeak returns nulls, not gaps.** When the rig is quiet the newest feed
  entries have `null` fields. `latest_non_null` looks back up to 100 entries for
  the last populated value.
- **OM2M is expected to be down.** Every call has a short timeout and a refusal
  is a normal outcome shown in the UI, not an error.
- **`legacy/smart_grid_php/` is not maintained.** It is the original site, kept
  for reference. It has SQL injection throughout and stores passwords in plain
  text; do not deploy it.
- **`hardware/` was not changed in the refactor.** The sketches cannot be
  compiled or flashed from here, so they were left as they are.

## Continuous integration

`.github/workflows/ci.yml` runs on every push to `main` and every pull request.

| Job | What it runs |
|---|---|
| `test` | `ruff check .` then `pytest -q`, on Python **3.11** and **3.12** |
| `audit` | `pip-audit -r requirements.txt`, blocking |
| `secrets` | Two regression checks, below |

The audit reads `requirements.txt` rather than the installed set, so a dev-only
advisory cannot fail an unrelated change while a runtime one still does.

**The `secrets` job exists because this repository has leaked credentials
twice.** It fails if either:

1. a credential-shaped literal (`api_key = "..."`, `MQTT_PASSWORD = "..."`)
   appears in the tree, or
2. **any database file is tracked** (`*.db`, `*.mv.db`, `*.sqlite`).

The second check is the important one. `legacy/om2m-database/indb.mv.db` held
the ThingSpeak read and write keys and the demo passwords in plain text, in
HEAD, and survived the pass that took those keys out of the source because it is
a binary file and no text scanner looks inside one. A binary blob is where a
secret hides.

## Documentation

| File | For |
|---|---|
| `README.md` | Users. Dark mode gallery |
| `README-light.md` | The same page in light mode. **Generated** |
| `DEVDOC.md` | This file. Contributors |
| `legacy/README.md` | What the archived PHP app and OM2M dump are, and why not to deploy them |
| `not_for_you.md` | The author's working log. Not documentation |

`README-light.md` is generated by `python scripts/build_light_readme.py`. Edit
`README.md`, run it, commit both. It exits non-zero if a marker it needs is
missing, so the light page cannot drift into pointing at the dark screenshots.
Python rather than Node so the repository needs no second toolchain.

Screenshots live in `docs/screenshots/{dark,light}` at 1440x900 and
`docs/screenshots/responsive/{dark,light}` at phone and tablet sizes.

**Clear the ThingSpeak keys before capturing the Profile page.** It renders them
in plain input fields, which is the point of the page and also means a
screenshot publishes them. A fresh clone shows them empty, since the seed reads
them from the environment.

## Licensing

MIT, see `LICENSE`. Runtime dependencies are Flask and `requests`, both
permissive.

The `legacy/` tree is archived code from earlier versions of this project. It is
covered by the same licence but should not be deployed: `legacy/README.md`
explains why.
