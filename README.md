<p align="center">
  <img src="./gridwatch/static/img/logo-mark.png" width="96" alt="ADK DEV">
</p>

# GridWatch

A web front end for a smart energy grid rig: it shows what every appliance on the
circuit is doing, scores its condition, raises alerts when something looks wrong,
and lets a resident switch appliances on and off from anywhere.

The rig itself is a set of ESP boards driving motors, LEDs and buzzers through
relays, with current and temperature sensors on each branch. Readings go to a
ThingSpeak channel; control commands come back through an OM2M gateway or the
same channel. GridWatch is the part a person looks at.

For architecture, data model and setup, see **[DEVDOC.md](./DEVDOC.md)**.

## Features

### Dashboard
- Every appliance as a card: power, speed, direction, current draw, temperature.
- Switch power, speed and direction from the card. The change is pushed to the
  hardware and the page updates without a reload.
- Summary tiles for appliances on, total draw, overall health and the age of the
  most recent reading.
- The page keeps polling in the background, and stops while the tab is hidden.

### Health
- A condition score of 1 to 3 per appliance, shown as a chart and as a table.
- The rig reports 0 for appliances it has not scored; those gaps are filled in
  and labelled rather than left blank.

### Statistics
- Current draw per appliance over time, all series on one axis with a shared
  crosshair.
- Latest, minimum, maximum and mean per appliance underneath.

### Notifications
- Raised automatically: an appliance drawing power while switched off reads as
  theft; draw drifting from the rated current reads as wear.
- The same alert is not raised twice within half an hour.
- Mark individual alerts read or unread, or clear them all.

### Profile
- Change the ThingSpeak channel, field number and API keys.
- Set the appliance list and its load-shedding order.
- Change your password.
- See the last ten control commands and whether they were delivered.

### Administration
- An administrator sees every resident: channel, appliances on, total draw,
  health, unread alerts and whether their data is live.

## Roles

| Role | Can do |
|---|---|
| **Resident** | Everything above for their own channel |
| **Administrator** | The same, plus a read-only view of every resident |

## Where the data comes from

Each page tells you what it is showing:

| Badge | Meaning |
|---|---|
| **Live** | Appliance state was read from ThingSpeak just now |
| **Cached** | ThingSpeak had nothing, so the last state GridWatch recorded is shown |
| **Simulated readings** | The boards have not published recently, so sensor values and health scores are stand-ins derived from the appliance state |
| **OM2M** / **OM2M offline** | Whether the local gateway is reachable |

Simulation exists so the interface is legible when the rig is powered down. It is
always labelled, and `GRIDWATCH_SIMULATE=0` turns it off, at which point empty
readings show as empty.

## Demo accounts

A fresh database is seeded with:

| Email | Password | Role |
|---|---|---|
| `Resident1@students.iiit.ac.in` | `password1` | Resident |
| `Resident2@students.iiit.ac.in` | `password2` | Resident |
| `admin@students.iiit.ac.in` | `admin` | Administrator |

These are demo credentials for a teaching rig. Change them before running this
anywhere that matters.

## Running it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py
```

Then open http://127.0.0.1:5000. The database is created and seeded on first run.

## Repository layout

| Path | What is in it |
|---|---|
| `gridwatch/` | The Flask application |
| `tests/` | Test suite |
| `hardware/` | Arduino sketches for the ESP boards |
| `legacy/smart_grid_php/` | The original PHP site, kept for reference |
| `legacy/om2m-database/` | H2 database files from the OM2M gateway |
| `docs/` | Project presentation |

## Tech stack

Python 3.12, Flask 3, SQLite, Jinja templates, hand-written CSS with light and
dark themes, and Chart.js for the charts. No build step and no front-end
framework.
