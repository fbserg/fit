# Watch data: Samsung Health → this repo, continuously

Researched 2026-08-12. The goal is a loop that runs without anyone touching it, matching the
Liftosaur pull already in `tools/daily_pull.sh` — not a manual export whenever someone remembers.

## The pipeline

```
Galaxy Watch
   └─ Samsung Health            (phone)
        └─ Health Connect       (Android 14+, nightly scheduled export)
             └─ "Health Connect.zip"   ← unencrypted SQLite, full snapshot
                  └─ OneDrive          (phone app)
                       └─ OneDrive sync
                            └─ ~/Library/CloudStorage/OneDrive-Personal/HealthConnect/
                                 └─ tools/health_connect.py   → data/health/*.jsonl
```

No third-party app, no API keys, no OAuth, no paid tier. OneDrive was chosen over Google Drive for
one reason: it is *already* syncing to this Mac, so the transport needed zero new infrastructure.

## Why this and not something better

There is nothing better. The options, and why each loses:

| Path | Verdict |
|---|---|
| **Health Connect scheduled export** | **Chosen.** First-party, free, daily/weekly/monthly, unencrypted SQLite. |
| Samsung Health API | Partner-gated. Not available to individuals. |
| Health Connect API | Android-only, and **no cloud API exists** — unreachable from a Mac at all. |
| `adb` off the phone | Samsung Health lives in `/data/data/com.sec.android.app.shealth/` with `allowBackup=false`. Needs root. |
| Google Takeout | Omits Health Connect entirely. |
| Samsung Health manual export | Works, but it is manual — the thing this document exists to avoid. |
| Health Sync (third-party) | Produces cleaner CSVs and is a real fallback, but it is a paid app and an extra hop for data the native export already carries. |

**The load-bearing constraint:** Health Connect is Android-only with no cloud API, so unlike
Liftosaur there is no way to *fetch* this data. It has to be *pushed* to us. Every viable design is
therefore some phone-side scheduled job writing to storage we can see, and the only question is
which one. Google shipped that job natively, so use it.

## Setup (phone side — the part that cannot be automated from here)

1. **Samsung Health → Settings → Health Connect** — turn on syncing and grant write permission for
   the types below. Samsung writes: steps, distance, calories, exercise sessions, heart rate, HRV,
   resting heart rate, SpO2, sleep sessions and stages, weight, height, nutrition, hydration.
2. **Health Connect → Backup and restore → Scheduled export** — set **daily**, save to **OneDrive**.
   Requires Android 14+.
3. Confirm it lands in a folder OneDrive syncs, then check from here:
   `python3 tools/health_connect.py schema`. That prints a `mapping check` block — hand-verify it
   against the table in "Schema, and how it was established" below before trusting any ingested
   row. This is the one verification the test suite cannot do for you.
4. Nothing else. `ingest` is written, tested, and already wired into `tools/daily_pull.sh` — the
   loop starts on its own the first night an export lands.

**Also check, once, on the phone:** Health Connect → Manage data → **Auto-delete must be OFF**
(it is off by default). Health Connect retains data indefinitely unless auto-delete is on, which
is what makes a missed week recoverable — the next snapshot still contains it. With auto-delete
on, history is silently truncated and no amount of correctness here gets it back. Note the widely
repeated "Health Connect only keeps 30 days" claim is about a *connected app's read window*
through the permissions system, not about storage, and does not apply to the scheduled export.

## Failure modes, and what shouts

The pipeline's real risk is not corruption, it is silence. A stopped export looks exactly like a
quiet week. `daily_pull.sh` distinguishes three states deliberately:

| State | Behaviour | Why |
|---|---|---|
| Phone setup never done (no `data/health/raw/*.zip` yet) | **Silent.** Ingest fails, job still exits 0 | Absence is the expected state before step 1–2 happen. Crying wolf nightly over a known-pending task trains you to ignore it |
| Export landed once, then ingest fails | **Loud notification**, non-zero exit | The pipeline was live and broke |
| Ingest succeeds but the newest zip is >48 h old | **Loud notification**, non-zero exit | OneDrive keeps serving yesterday's file quite happily. A successful ingest of a stale zip is precisely what a stopped phone export looks like, and it is the failure mode most likely to go unnoticed for a month |

## Schema, and how it was established

Table mapping derived 2026-08-12 from AOSP `packages/modules/HealthFitness`
(`service/java/com/android/server/healthconnect/storage/datatypehelpers/*RecordHelper.java`),
corroborated independently by two working third-party parsers that agree on every table name they
touch. Graded per `PLAYBOOK.md` rule 16 — **A** where read in AOSP source, **B** where only
third-party parsers confirm.

| Record | Table | Grade |
|---|---|---|
| Sleep session | `sleep_session_record_table` | A |
| Sleep stages (**discarded**) | `sleep_stages_table` | A |
| Resting heart rate | `resting_heart_rate_record_table` | **B** — built from a constant, literal string not readable in source; the ingest tries both spellings and reports which it found |
| Heart rate samples | `heart_rate_record_series_table` (`epoch_millis`, `beats_per_minute`) | A |
| Weight | `weight_record_table` | A |
| Steps | `steps_record_table` | A |
| Exercise session | `exercise_session_record_table` (`exercise_type`; **squash = 43**) | A |
| Body fat / water / lean / bone (**quarantined**) | `*_record_table` | A |

Mechanics worth knowing:

- **Every record carries a `uuid` BLOB** — that is the upsert key, hex-encoded on the way out.
- **Times are epoch milliseconds with a *separate* zone-offset column in seconds**, never a
  combined local timestamp. The ingest recombines them so nothing downstream has to know.
- **Origin app** comes from `app_info_id` joined to `application_info_table`, which is how a
  Samsung Health row is told apart from anything else writing to Health Connect.
- **There is no foreign key from an exercise session to heart rate.** Correlating a squash game
  to its HR is a time-range join done in application code — the ingest does it and stores mean,
  max and sample count per session. That is the measurement that upgrades `cardio.md` §9's
  squash energy figures from C-grade MET lookups to something derived from this player.
- The schema has an `onUpgrade` path and has changed across module releases, so the ingest
  **resolves tables by introspection at run time** rather than hardcoding, and fails loudly on a
  database that is not a Health Connect export rather than silently writing zero rows.

Unresolved, flagged rather than guessed: the current `DB_VERSION` integer and a changelog of prior
schema diffs could not be pinned. Introspect-first is the defensive posture that makes that
survivable.

## Test

`python3 tools/test_health_connect.py` builds a synthetic export to the schema above and asserts
the mapping, the zone-offset round trip, hex uuids, the HR time-window join, upsert idempotence,
the staleness gate, and that a foreign database fails loudly. It exists because the first night of
real data should not also be the first test of the code reading it.

**It proves the code does what it intends against the schema it believes in — not that the schema
is right.** Only step 3 above can do that.

## What to take, and what to refuse

| Data | Use | Why |
|---|---|---|
| **Sleep duration** | Yes | Largest unmeasured input in the project. Total sleep time is ~80–90% valid against polysomnography. |
| **Resting heart rate** | Yes | Genuine recovery/overreaching trend, and wrist RHR is one of the things these devices measure *well*. |
| **Weight** | Yes, if present | Would close the nutrition calibration loop. Only appears if entered manually or via a Samsung scale. |
| **Steps** | Trend only | NEAT proxy for the TDEE problem. Never the device's kcal figure — that is a derived number with an unaudited chain. |
| **Exercise sessions (squash)** | Yes | `AGENTS.md` flags squash as known-regular with no analysis. HR data would finally let `cardio.md` price it. |
| Sleep **stages** | No | Duration is decent; REM/deep staging is not. Take the total, discard the breakdown. |
| **Body fat / body water / lean mass** | **Never** | This is the Galaxy Watch's wrist BIA. Quarantined in the ingest by constant, not by convention — see below. |

### The BIA trap

The Galaxy Watch (4 and later) does wrist BIA, Samsung Health writes it, and Health Connect carries
it — so it *will* arrive in every export whether or not anyone wants it. `AGENTS.md` already rules
that BIA absolutes are untrustworthy and that measurement methods are never compared across
devices. A wrist BIA is strictly worse than the InBody, and letting the two into the same trend
would corrupt the only body-composition series this project has.

It is dropped at ingest via `QUARANTINED_RECORD_TYPES`, deliberately, rather than filtered later at
analysis time — where someone would eventually forget, notice a tempting daily body-fat number, and
plot it.

## Ingestion shape

Each export is a **full snapshot, not a delta**. So ingestion mirrors the Liftosaur pull exactly
(`DECISIONS.md`, "Results store: append-only JSONL"): archive the raw zip by date under
`data/health/raw/`, then upsert canonical rows keyed by record id. Re-ingesting the same zip is a
no-op, and a missed day self-heals on the next run because the next snapshot still contains it.
