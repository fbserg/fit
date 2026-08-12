# Training history before this repo

Everything logged before 2026-02 lives in Hevy. This is what it actually says, and what it is and
is not evidence for.

Exported 2026-07-31. Raw CSV and the converted JSONL are in `data/hevy/` — gitignored, because the
repo is public and workout logs are not. This file holds the derived findings, which are.

## Getting the export

Hevy's export is free and needs no subscription. On the web: **hevy.com → Settings → Export Data →
Export Workout Data**. It assembles the CSV in the browser from paged
`api.hevyapp.com/workouts_batch/<cursor>` calls and downloads it; there is no export URL to hit
directly, and the API rejects cross-origin fetches. So this one stays a manual click — which is
fine, it happens once.

Then:

```bash
python3 tools/hevy_csv.py data/hevy/workouts-<date>.csv
```

That converts one-row-per-set CSV into the same flattened JSONL shape
`tools/liftosaur.py snapshot` writes, so analysis reads one format across both eras.

## What the log contains

**64 workouts, 1236 sets, 45 distinct exercises, 2024-07-22 → 2026-02-03.**

| | | | |
|---|---|---|---|
| 2024-07 **6** | 2024-08 **2** | 2024-09 **2** | *— 9-month gap —* |
| 2025-06 **15** | 2025-07 **8** | 2025-08 **5** | 2025-09 **6** |
| 2025-10 **9** | 2025-11 **4** | 2025-12 **2** | 2026-01 **4** |
| 2026-02 **1** | *— nothing since —* | | |

Two things jump out.

**The consistency claim holds, and the shape is worse than "inconsistent" suggests.** The June 2025
block starts at 15 sessions/month and decays monotonically to 1. That is not random inconsistency;
it is a program losing traction. Whatever `program.md` is, its job is to not do that — which is why
`loop.md` checks adherence at all, not just progression.

**The last logged session was 2026-02-03, about six months before this repo's baseline scan.**
Two readings and the data cannot separate them: training stopped, or logging stopped. The scan
cannot separate them either — skeletal muscle mass rose 75.2 → 76.5 lb across the whole 14.7-month
window, and mass persists through a detraining gap of this length even when strength does not.

This does **not** overturn the one-week ramp (`DECISIONS.md`). That ruling rests on retained muscle
mass, which is measured and still true. It does change what the ramp is *for*: not rebuilding
tissue, but re-establishing technique and connective-tissue tolerance at loads the muscle can
already handle.

## The dumbbell units trap

**Hevy logged dumbbell lifts as combined weight; Liftosaur wants the weight of one dumbbell.**
Every dumbbell number below is therefore halved on the way into the program, and getting this
backwards is a 2× error in either direction.

The export does not say which convention it used, so it was settled by internal consistency —
three independent checks, all agreeing:

| Check | Reading as *total* | Reading as *per hand* |
|---|---|---|
| Incline DB press 80 vs barbell bench 125 × 5 | 40/hand — normal ratio | 160 total — would imply a ~200 lb bench |
| DB shoulder press 70 vs barbell OHP 65 | 35/hand — DB total slightly above barbell, as expected | 140 total vs a 65 lb barbell press |
| Single Arm Tricep Extension 15 | one dumbbell, consistent by definition | same |

Liftosaur's side is not a guess: `src/models/settings.ts` gives `dumbbell` a `multiplier` of 2 and
a 10 lb bar — the same structure as `barbell` (multiplier 2, 45 lb bar). The multiplier is the two
loadable sides of *one* implement, so the entered weight is one dumbbell.

Incidentally this confirms the gym has 2.5 lb dumbbell steps: the logged lateral-raise totals run
12.5 / 15 / 20 / 25 / 30 / 35, which is 6.25 / 7.5 / 10 / 12.5 / 15 / 17.5 per hand.

## Starting loads

Week-1 loads now live in `program.liftoscript`. This is where they came from.

Every reference below is the last logged session for that movement, and the intra-session rep
drop-off (bench 115 × 8, 5, 5) says these sets were taken at or near failure — so they are
near-maximal, not comfortable. Three things then push the starting load *down* from them: roughly
six months since the last logged session, a program that runs more sets per exercise than the old
one (5 where he did 3), and an explicit ramp week. Three things are neutral or push *up*: muscle
mass was retained, the last-logged numbers were already depressed by the adherence decay
(bench peaked at 125 × 7 in October and fell to 115), and the target is 1–2 RIR rather than failure.

Net: start ~10–15% under the last logged working weight, except where the movement itself changed.

| Program exercise | Hevy reference | → per hand | **Week 1** | Basis |
|---|---|---|---|---|
| Incline Bench Press, DB | Incline BP (DB) 80 × 10 | 40 | **35 lb** | A |
| Incline Row, DB | Chest Supported Incline Row (DB) 60 × 12 | 30 | **25 lb** | A |
| Lateral Raise, DB | Lateral Raise (DB) 30 × 10 | 15 | **12.5 lb** | A |
| Bicep Curl, DB | Bicep Curl (DB) 45 × 10 | 22.5 | **20 lb** | A |
| Lat Pulldown, Cable | Lat Pulldown (Cable) 115 × 6 | — | **100 lb** | A |
| Romanian Deadlift, BB | RDL (BB) 115 × 8 | — | **95 lb** | A |
| Seated Leg Curl, Machine | Seated Leg Curl 100 × 12 | — | **85 lb** | A |
| Standing Calf Raise, Machine | Standing Calf Raise (Machine) 170 × 12 | — | **150 lb** | A |
| Reverse Fly, Machine | Rear Delt Reverse Fly (Machine) 70 × 12 | — | **55 lb** | A |
| Bench Press, DB | *from* Incline DB 40/hand + barbell bench 115 | — | **40 lb** | B |
| Triceps Extension, Cable | *from* Pushdown 42.5 × 12, ×0.6 for overhead | — | **25 lb** | B |
| Bulgarian Split Squat, DB | *from* Squat (BB) 105 × 10 | — | **20 lb** | C |
| Leg Press, Machine | *from* Hack Squat 140 × 6 | — | **180 lb** | C |

**A** — direct data, same movement. **B** — the movement changed, so a transfer factor dominates
the staleness. The triceps case is the big one: the program calls for an *overhead* cable
extension and the history is all pushdowns, which are far stronger through that range.
**C** — no data for the movement or anything close. Bulgarian split squats and leg presses were
never logged.

**The two C rows are guesses and the leg press is the worst of them.** Leg press loading is
machine-specific to the point of being incomparable — sled weight, angle, and plate-vs-selectorized
all move it by more than the training effect does. Expect to correct it inside the first set. The
split squat is limited by balance rather than load in week 1 regardless of what the number says.

None of these carry an RPE, so there is no way to know whether `80 lb × 10` was a grinder or had
four in reserve. Treat the whole table as a starting point that double progression will correct
within two or three sessions — its real job is catching a wildly wrong first guess, not being right.

**Scored against the first real Day 3 (2026-08-11).** The table's job was catching a wildly wrong
guess, so here is how the two C rows and the balance claim actually did:

| Prediction | Outcome |
|---|---|
| Split squat 20 lb (C) | **Right.** Sets 2–4 were 8 reps at RIR 1 — bottom of the 8–12 range, no correction needed. A confidence-C guess from a barbell squat landed. |
| "Limited by balance rather than load" | **Wrong.** Balance was a non-issue; the report was "massive pump, very hard to walk". Load-limited from set one. |
| RDL 95 lb from 115 × 8 (A) | **Wrong for an unmodelled reason.** He trained 90 and the limiter was grip, not hamstrings — the table extrapolates the target muscle and is blind to whichever tissue actually fails first after six months off. |

The lesson is the third row: a starting-load table transfers *strength at the prime mover* and
silently assumes every supporting link came back at the same rate. Grip did not.

## A progression bug that only appeared once the weights were real

Writing concrete loads exposed something the abstract program could not show: `dp(5lb, …)` on a
dumbbell lift means 5 lb *per hand*, which on small isolation movements is an enormous jump.

| Lift | Was | Jump | Now |
|---|---|---|---|
| Lateral Raise | dp(5lb) | 12.5 → 17.5/hand, **+40%** | dp(2.5lb) |
| Bicep Curl | dp(5lb) | 20 → 25/hand, **+25%** | dp(2.5lb) |
| Incline Row | dp(5lb) | 25 → 30/hand, +20% | dp(2.5lb) |
| Incline Bench Press | dp(5lb) | 35 → 40/hand, +14% | dp(2.5lb) |
| Bench Press | dp(5lb) | 40 → 45/hand, +12.5% | dp(2.5lb) |

A 40% load jump on a lateral raise doesn't get earned; it stalls the lift for months. The history
shows exactly that happening — lateral raises sat at 30 lb total from August 2025 to February 2026
with reps *declining* (12 → 10 → 8), which is what a too-large next step looks like from the inside.

Bulgarian split squat keeps `dp(5lb)`: it's a lower-body movement where a 5 lb/hand step is a
smaller relative jump, and legs tolerate coarser increments. Barbell, cable and machine lifts are
unchanged — their increments were already sane relative to their loads.

## What this history cannot do

- **No RPE anywhere.** The Hevy export has an `rpe` column and it is empty in all 1236 rows — RPE
  is opt-in per set and was never entered. `loop.md`'s stall detection is RIR-based, so it cannot
  run against any of this. Load and volume only.
- **No bodyweight for 114 working sets** — dips, planks, leg raises, rowing and stair machine.
  Recorded as null, never zero, so they don't silently deflate a volume average.
- **Not imported into Liftosaur.** Liftosaur has a native Hevy CSV importer
  (`src/utils/importFromHevy.ts`, 259-entry name map, dedupes by start time, undoable). It would
  drop the exercise-name nuance above and cannot carry RPE either. The archive plus this file
  covers what the history is actually good for, without putting 64 unverifiable sessions into the
  account the weekly review reads from. Reopen if a cross-era chart is wanted badly enough.
