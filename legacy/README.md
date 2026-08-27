# Archived

Nothing in this directory is maintained or deployed. It is kept so the original
work stays readable next to the current application.

## `smart_grid_php/`

The original PHP site, as it ran on 000webhost. GridWatch replaced it; every
feature it had (dashboard, health, statistics, circuits, notifications, user
profile, about, admin overview, signup) now lives in the Flask app at the
repository root.

Do not deploy it. It builds SQL by string concatenation on request data, stores
passwords in plain text, and has API keys committed in the source.

## `om2m-database/`

H2 database files from the OM2M gateway the ESP boards published to. Useful only
if you want to bring that gateway back up.
