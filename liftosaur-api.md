# Liftosaur: getting programs in and data out, without clicking

Derived 2026-07-31 by reading the open-source server (`github.com/astashov/liftosaur`, `lambda/index.ts`)
and the deployed client bundle (`https://www.liftosaur.com/app.js`). Every claim below has a source
line behind it. Nothing here is inferred from docs alone.

## The short version

There are three ways to write a program to an account. Two are official and cost money. One is free.

| Route | Auth | Cost | Verdict |
|---|---|---|---|
| **Official MCP server** (`https://www.liftosaur.com/mcp`) | OAuth 2.1 or `lftsk_` API key | **Premium subscription** | Best if paying. ~40 tools incl. `update_program`, `get_history`, `get_program_stats`, `run_playground`. |
| **REST API** (`/docs/api`) | `lftsk_` API key | **Premium subscription** | Same gate, less useful than MCP. |
| **App's own internal endpoints** | `session` cookie | Free | What we use. Three calls, plain JSON. |

The premium gate is real and enforced server-side, not a docs suggestion:

- `lambda/mcp/handler.ts:308-311` — `hasSubscription(...)` → `"Active subscription required to use MCP tools"`
- `lambda/utils/apiKeyAuth.ts:57-60` — `"Active subscription required to use the API"`

Creating an API key is *not* gated (`lambda/index.ts:2095-2109` checks auth only), so you can mint a
`lftsk_` key for free. It just won't authorize anything until you have a subscription. Don't be fooled
by the key appearing to work.

## The free path

Everything below is authenticated by one cookie: **`session`** — `lambda/dao/userDao.ts`,
`getCurrentUserIdFromCookie` reads `cookies.session` and nothing else. It is `httpOnly`, so it cannot
be read from page JavaScript; it has to come out of the browser's cookie store.

### 1. Read everything

```
GET https://api3.liftosaur.com/api/storage
Cookie: session=...
```

Returns the complete `IStorage` — settings, programs, full history, stats — plus top-level `email`
and `user_id`. This is the weekly-review data source. Not premium-gated.

### 2. Write a program

```
POST https://api3.liftosaur.com/api/program
Cookie: session=...
Content-Type: application/json

{
  "program": {                       // <- an IExportedProgram, NOT an IProgram
    "program":         { ...IProgram, "planner": { "weeks": [...] } },
    "version":         "<storage.version>",   // MUST equal the server's storage.version
    "settings":        { ... },
    "customExercises": { }
  },
  "deviceId": "fit-repo",
  "source":   "fit-repo"
}
```

Handler: `lambda/index.ts:1586-1707`. Returns `200 {"data":{"id":"..."}}`.

The two failure modes, both of which we hit:

- `400 {"error":"Version mismatch! Please refresh the page."}` — `index.ts:1606`. The comparison is
  `oldStorage.version !== exportedProgram.version`. It is the **storage schema version**
  (e.g. `"20260702120000"`), not a program version, and it lives on the *envelope*, not inside
  `program`. Fetch it from `/api/storage` immediately before writing.
- `409 "Your program is out of date"` — `index.ts:1611-1629`. The program's `clonedAt` is in the
  account's tombstone map. Re-read storage and retry.

Putting `version` inside the inner `program` object instead of on the envelope gives a `500`, because
the program object is schema-validated. The shape is strict.

Note `index.ts:1632-1635`: the server preserves the account's `nextDay`, overwriting whatever you
send. You cannot accidentally rewind someone's position in the program by re-uploading it. Good.

**This endpoint replaces; it does not append.** The merge is
`CollectionUtils_setBy(oldStorage.programs, "id", program.id, program)`, and `setBy`
(`src/utils/collection.ts:293-300`) is a plain `.map()` — if no existing program has that id,
the array comes back unchanged and the write silently does nothing. So always target the id of a
program that is already in the account. Getting the *first* program in is a one-time job for the
web UI ("Add this program to your account" on a `/p/<hash>` page); after that everything is
scriptable. `tools/liftosaur.py` enforces this by refusing to invent ids.

`DELETE /api/program/:id` exists (`index.ts:1709`) for removing a program.

### 3. Set the active program

`POST /api/program` does not touch `currentProgramId`. That lives in storage and needs a sync:

```
POST https://api3.liftosaur.com/api/sync2
Cookie: session=...

{
  "storageUpdate": {
    "version":  "<storage.version>",
    "versions": { "currentProgramId": <now-ms> },   // must beat the server's clock for this field
    "storage":  { "currentProgramId": "<programId>" }
  },
  "deviceId": "fit-repo",
  "timestamp": <now-ms>,
  "historylimit": 20
}
```

Two things make this much less scary than it looks:

- **The gzip is optional.** `index.ts:541-546` — if the body has no `data` string, the raw JSON body
  is used directly. The client always compresses (`Encoder_encode` = gzip → base64 data-URI → base64);
  we don't have to.
- **Merging is per-field last-write-wins**, not whole-storage replacement.
  `userDao.applySafeSync2` → `VersionTracker.mergeByVersions(serverStorage, serverVersions,
  updateVersions, updateStorage)`. Send one field with one timestamp and only that field moves.
  Omitting a field means "no opinion", not "delete".

Two traps in that merge, both silent — no error, the data just doesn't land:

- **`versions` is the gate, not `storage`.** The merge loop iterates
  `Object.keys(storageUpdate.versions)`, *not* the keys of `storageUpdate.storage`
  (`versionTrackerMergeByVersions.ts:31-86`). A field present in `storage` but absent from
  `versions` is never even looked at. Both halves must name the field.
- **Programs are keyed by `clonedAt`, not `id`, inside the collection merge.**
  `VersionTrackerUtils_getId` reads `obj.vtype` → `TYPE_ID_MAPPING.program = "clonedAt"`. A program
  object with no numeric `clonedAt` gets dropped from the merge entirely. `id` is still what
  `currentProgramId` and `Program_getProgram` key off — the two identifiers serve different systems
  and both must be present.

Also note `applySafeSync2` validates the *pre-merge* server storage, not the post-merge result
(`userDao.ts:245` vs `278-391`). There is no schema safety net on what you write. Build a
conformant object; nothing will stop you if you don't.

Omit `originalId` and you take the "merging" branch (`index.ts:600-652`), which is the normal
multi-device path and returns the full merged storage back — a free read-after-write check.

## The tools

Two scripts, no dependencies beyond the standard library and the `openssl` binary macOS ships with.

```bash
python3 tools/extract_cookie.py                       # refresh auth (the only maintenance task)
python3 tools/liftosaur.py doctor                     # check every link, name the fix
python3 tools/liftosaur.py status                     # account, active program, history count
python3 tools/liftosaur.py pull > scans/storage.json  # everything, for the weekly review
python3 tools/liftosaur.py push program.liftoscript   # repo text -> account, verified
python3 tools/liftosaur.py push-share 11b2a78c        # import a /p/<hash> link instead
python3 tools/liftosaur.py activate <programId>
```

`push` is the one that matters: it splits a Liftoscript file on its `# Week` / `## Day` headers,
splices the result into the account program's `planner.weeks`, and reads the program back to confirm
the content actually landed. That closes the loop from repo → phone with no clicking.

### Keeping it working

The whole maintenance story is one command with no arguments:

```bash
python3 tools/extract_cookie.py
```

It finds the `session` cookie in every Chrome profile, decrypts it, **verifies it against the live
API before overwriting the existing file**, and writes it mode 600. A failed extraction leaves the
previous working cookie untouched. First run pops a Keychain prompt — choose "Always Allow" and later
runs are silent.

Run it when `liftosaur.py` reports a 401. There is no schedule to keep: sessions last a long time and
the failure is loud, so waiting for the error is correct rather than lazy.

`doctor` is the other half. It walks the chain — cookie present, file permissions, API auth, an active
program that actually exists, no ambiguous same-named programs, the repo script parses, and **the
account's program matches `program.liftoscript`** — and prints the exact command to fix whichever
link is broken. That last check is the one worth having: it catches drift from someone editing the
program in the app, which is otherwise invisible until a weekly review quietly analyses the wrong
program. Exit code is nonzero on failure, so a scheduled job can gate on it.

### How the cookie extraction works

The cookie is `httpOnly`, so no page script can read it. Chrome encrypts cookie values on macOS with
a key held in the Keychain under `Chrome Safe Storage`. The derivation is fixed in Chromium and not
itself secret: PBKDF2-HMAC-SHA1 of the Keychain password with salt `saltysalt`, 1003 iterations,
16-byte key, then AES-128-CBC with a 16-space IV. Key derivation is stdlib `hashlib`; the AES step
shells out to `openssl` so there is no pip dependency to install or break.

Two details that will bite anyone reimplementing this:

- **Chrome 127+ prepends a 32-byte SHA-256 domain hash** to the decrypted plaintext; older versions
  don't. Rather than sniff the version, the script tries both offsets and keeps whichever yields a
  usable cookie.
- **The API sits behind a WAF that rejects unknown user agents with a 403** before it ever looks at
  the cookie. Python's default `Python-urllib/3.x` gets blocked, which reads like an auth failure and
  isn't. Both scripts send a browser user agent and report 403 and 401 as distinct problems.

Treat `.liftosaur-session` as a password — it is full read/write on the account. It is gitignored and
written mode 600. If it leaks, sign out in the Liftosaur app; that invalidates it immediately.

## What we deliberately did NOT do

- **Reimplement `Sync_getStorageUpdate2`.** The client builds a full vector clock across every storage
  field via `VersionTracker.diffVersions/extractByVersions/fillVersions`. Getting it wrong can silently
  drop or clobber data. For single-scalar edits the hand-built one-field `versions` object above is
  enough, and the blast radius is one field.
- **Drive the mobile-web app UI.** `https://www.liftosaur.com/app/` is React Native Web: every control
  is an unlabeled `<div>`, and it uses pointer/touch responders, so synthetic `.click()` and plain
  coordinate clicks are both no-ops. If you must automate it, dispatch a real
  `pointerdown`/`pointerup` pair; that works where clicking does not.
- **Scrape the public profile page.** It serves the same data with no auth, but it publishes your
  email and subscription receipt. Rejected in `loop.md`.

## The browser fallback, if the cookie route ever breaks

The **web editor** at `https://www.liftosaur.com/user/p/<programId>` is a normal DOM page — real
`<button>` elements, and stable `nm-*` class hooks the app adds for its own analytics. The save button
is `.nm-web-save-planner`. That page handles the version/sync protocol itself, so a Playwright script
that edits the CodeMirror content and clicks that one selector is robust to protocol changes in a way
a hand-rolled sync client is not.

Prefer the HTTP route. Keep this one documented as the escape hatch.

## Daily automated pull (macOS)

`tools/daily_pull.sh` wraps `snapshot` for unattended daily runs: notification on new workouts,
loud notification on failure (a silently expiring session cookie must not read as "no workouts"),
silence when nothing changed. Install as a launchd user agent:

```sh
# plist at ~/Library/LaunchAgents/com.<you>.fit.dailypull.plist pointing at tools/daily_pull.sh,
# StartCalendarInterval daily, logs to private/daily_pull.log (gitignored). Then:
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<you>.fit.dailypull.plist
launchctl kickstart gui/$(id -u)/com.<you>.fit.dailypull   # test-fire once
```

Not committed: the plist itself (machine-specific absolute paths). A cloud/scheduled agent was
considered and rejected — the session cookie and `data/` baseline are deliberately local-only.

## Open decision

Whether to buy a Liftosaur subscription and use the official MCP server instead of any of this.
Reasons it might be worth it, given this repo's actual goal:

- `update_program` takes **Liftoscript source directly** — no `IProgram` construction, no envelope,
  no version dance.
- `run_playground` simulates a workout and validates progressions *before* saving. That would have
  caught the warmup-set problem without a gym trip.
- `get_program_stats` returns per-muscle weekly volume and per-day duration — the two numbers this
  repo currently derives by hand and argues about.
- It is a supported interface with a changelog, versus three undocumented endpoints that can move
  without notice.

Against: it costs money, and the free path demonstrably works today.
