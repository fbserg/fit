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
   `python3 tools/health_connect.py schema`
4. Once the schema is known, `ingest` gets written and folded into `tools/daily_pull.sh`.

## What to take, and what to refuse

| Data | Use | Why |
|---|---|---|
| **Sleep duration** | Yes | Largest unmeasured input in the project. Total sleep time is ~80–90% valid against polysomnography. |
| **Resting heart rate** | Yes | Genuine recovery/overreaching trend, and wrist RHR is one of the things these devices measure *well*. |
| **Weight** | Yes, if present | Would close the nutrition calibration loop. Only appears if entered manually or via a Samsung scale. |
| **Steps** | Trend only | NEAT proxy for the TDEE problem. Never the device's kcal figure — that is a derived number with an unaudited chain. |
| **Exercise sessions (squash)** | Yes | `CLAUDE.md` flags squash as known-regular with no analysis. HR data would finally let `cardio.md` price it. |
| Sleep **stages** | No | Duration is decent; REM/deep staging is not. Take the total, discard the breakdown. |
| **Body fat / body water / lean mass** | **Never** | This is the Galaxy Watch's wrist BIA. Quarantined in the ingest by constant, not by convention — see below. |

### The BIA trap

The Galaxy Watch (4 and later) does wrist BIA, Samsung Health writes it, and Health Connect carries
it — so it *will* arrive in every export whether or not anyone wants it. `CLAUDE.md` already rules
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
