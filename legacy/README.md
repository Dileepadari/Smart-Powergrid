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

**These files are no longer tracked.** `indb.mv.db` held the ThingSpeak read and
write API keys and the demo passwords in plain text. It survived the pass that
took those keys out of the source because it is a binary file and neither
`grep` nor a secret scanner looks inside one. They are gitignored now.

They are still in git history and on the machine that produced them, so nothing
is lost. **The keys they contain must be treated as public and rotated at
ThingSpeak**, since they were in a public repository.
