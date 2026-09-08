# not_for_you.md

A personal working log. Not documentation, and nothing here is needed to use or contribute to GridWatch. Everything a newcomer actually needs is in [README.md](./README.md) and [DEVDOC.md](./DEVDOC.md).

---

## A leak the earlier secrets pass missed, because it was binary

An earlier pass moved the ThingSpeak channel keys and MQTT credentials out of the source and into the environment, and that work was correct as far as it went. It missed this:

```
legacy/om2m-database/indb.mv.db   2.8 MB, tracked, in HEAD
```

Inside it, in plain text:

```
,Resident1@students.iiit.ac.in,password1,resident,2165368,6,EFISS04IFA6364N9,899FMRYW1H2FPCNJ
,Resident2@students.iiit.ac.in,password2,resident,2165370,7,D3LNELVJ4YHFILVP,RLEHO8H1Z8C0I48Y
```

All four ThingSpeak keys and both demo passwords, in a public repository, in the current commit.

**It survived because `grep` does not look inside binaries and neither does a secret scanner that works on text.** The H2 file is a database dump from the archived OM2M gateway; nobody thinks of it as a document containing credentials, which is exactly why it kept them. Found it by running `strings` over the tracked binaries specifically because the repo's own `legacy/README.md` admits the PHP archive "has API keys committed in the source" and I wanted to know what else was in there.

Untracked both `.db` files (`git rm --cached`, still on disk, still in history) and gitignored them. CI now has a job that fails if any `*.db`, `*.mv.db` or `*.sqlite` file is tracked, because the general lesson is that **a binary blob is where a secret hides from every text-based check**.

The keys are still in git history and were public, so they must be rotated at ThingSpeak. That was already on the rotation list; this just means the exposure was broader and more recent than the list implies.

## Other things fixed

- **`LICENSE` did not exist.** MIT added.
- **No CI.** Added: ruff, 48 tests on Python 3.11 and 3.12, `pip-audit` against `requirements.txt`, and the two secret-regression jobs above.
- **11 lint findings**, all real: two unused imports, three deprecated `typing` imports that belong in `collections.abc`, two unused unpacked variables, a shebang on a non-executable file, and import ordering.
- **A sentence that did not survive its own fallback.** `statistics.html` rendered "The most recent readings for every appliance on channel not configured." The dashboard uses the same `or 'not configured'` default and reads fine there ("Channel not configured" is a label), but mid-sentence it is not English. The clause is dropped now instead of defaulted.

## A mistake worth recording

Fixing the unused `off` variable, I ran a blind `str.replace` for:

```python
off, on = NOMINAL_CURRENT[appliance.kind]
```

That line appears **twice** in `simulation.py`. In `current_for` the `off` value is used two lines later; in `health_for` it is not. The replace hit both and 17 tests went red with `NameError: name 'off' is not defined`.

Caught immediately because the suite runs in 13 seconds. The fix was to edit by line number after asserting the line's content. The lesson is the ordinary one: a textual replace over a whole file needs to be unique or anchored, and "it's just renaming an unused variable" is precisely when you stop checking.

## `pytest` did not work, only `python -m pytest`

Caught by CI, not locally, because I had been running `python -m pytest` all along.

`python -m pytest` puts the working directory on `sys.path`; a bare `pytest`
does not. So `from gridwatch import create_app` in `tests/conftest.py` raised
`ModuleNotFoundError` for anyone who typed the command most people type. DEVDOC
happened to document the `python -m` form, which is why nobody had hit it.

Fixed with a `pytest.ini` setting `pythonpath = .`, so both invocations work.
Fixing it in the repository beats special-casing the CI command, since the
person it actually bites is a new contributor running `pytest`.

Worth noting as a habit: **running a suite the convenient way can hide that the
documented way is broken.** CI running the bare command is what surfaced it.

## Notes

- `run.py` defaults to `GRIDWATCH_DEBUG=1`. That looks alarming but is correct: it is the documented development entry point, binds to `127.0.0.1`, and its docstring says to serve `gridwatch:create_app()` behind a real WSGI server in production. Left alone.
- With debug off, Flask caches templates, so a template edit needs a restart. Cost me one confused round of "the fix did not apply".
- The Profile page renders the ThingSpeak read and write keys in plain input fields. That is the point of the page, but it means a screenshot of it publishes them. Cleared the keys in the local demo database before capturing, which is also what a fresh clone now shows, since the seed reads them from the environment and defaults to empty.
- Screenshot scale is per browser window and has to be re-measured every session: take one screenshot and divide its width by `window.innerWidth`. It was 0.8078 in one session and 0.7875 in the next, and using the stale number silently crops the right-hand third of every capture.

## Open threads

- **The keys need rotating at ThingSpeak.** Nothing in this repository can do that.
- `legacy/smart_grid_php/` still contains the old PHP app, which the legacy README correctly says builds SQL by string concatenation and stores passwords in plain text. It is an archive and marked as one, but it is also 52 files of exploitable code in a public repo.
- The simulation fallback is deterministic per appliance and seed, which is what makes the screenshots reproducible, but it also means two people running the demo see identical "live" data.
