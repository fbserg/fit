# Decision ledger

Debated choices, resolved. Each entry: the ruling, what actually decided it, and what would
reopen it. Check here before re-litigating — several of these were argued twice already.

Training-content rulings live in `program.md`, `exercises.md`, `abs.md`, and `swimming.md`
alongside their evidence. This file is for the choices that span documents or that a reader
would otherwise assume were arbitrary.

---

## Tooling

### Liftosaur over Hevy
**Ruling.** Liftosaur.
**Why.** Hevy's free tier cannot express per-exercise progression rules; the paid tier was
declined. Liftosaur's entire program is one text file, which lets this repo be the source of
truth and reduces the app to a runner. Authoring, the web editor, link import, and JSON/CSV
export are all free and work without an account.
**Reopens if.** Liftoscript stops being able to express something the program needs. The known
gap today is myo-reps: mini-set structure isn't representable as set groups, so it lives in a
comment for the lifter to follow manually.

### The free cookie path, not the official MCP server or REST API
**Ruling.** Write to the account with three `session`-cookie-authenticated endpoints
(`GET /api/storage`, `POST /api/program`, `POST /api/sync2`), implemented in `tools/liftosaur.py`.
**Why.** Liftosaur ships an official MCP server and REST API, and both are the nicer interface —
but both are hard-gated on an active subscription, enforced server-side
(`lambda/mcp/handler.ts:308`, `lambda/utils/apiKeyAuth.ts:57-60`). The free path is verified
working against the live service and derived from their open source, not guessed.
**Trap worth remembering.** Minting an `lftsk_` API key is *not* subscription-gated
(`lambda/index.ts:2095`). The key appears to work and authorizes nothing. Don't take key
creation as evidence of access.
**Reopens if.** A subscription gets bought, or an endpoint moves. The MCP server's
`run_playground` (simulate a workout, validate progressions before saving) and
`get_program_stats` (per-muscle weekly volume, per-day duration) are exactly the two things this
repo currently computes by hand — that is the real argument for paying, not convenience.

### A text file plus an HTTP tool, not browser automation
**Ruling.** `program.liftoscript` is the source of truth; `tools/liftosaur.py push` writes it.
Playwright against the web editor is documented as a fallback only.
**Why.** Driving the app UI cost most of a session and failed repeatedly. The mobile-web app is
React Native Web: every control is an unlabeled `<div>` using pointer/touch responders, so both
synthetic `.click()` and coordinate clicks are no-ops. Real `pointerdown`/`pointerup` pairs do
work, which is worth knowing, but it is a bad foundation for something run weekly.
**Reopens if.** The undocumented endpoints break. The escape hatch is the web editor at
`/user/p/<programId>` — a normal DOM page with stable `nm-*` class hooks, save button
`.nm-web-save-planner` — which handles the sync protocol itself and so is more robust to protocol
change than a hand-rolled client.

### The authenticated storage endpoint, not the public profile page
**Ruling.** `GET /api/storage` with a cookie.
**Why.** The public profile page serves the same data with no auth, but publishes the account
email and subscription receipt, carries no `noindex`, and permits crawling. Email exposure was
accepted by the user for the repo, but that is not a reason to publish it to search engines.
**Reopens if.** Nothing foreseeable. This one is settled.

### The program is stored as text, so no compiler is needed
**Not a decision so much as a finding that removed a planned piece of work.** Liftosaur stores
programs at `planner.weeks[].days[].exerciseText` as raw Liftoscript. The legacy structured
`weeks`/`days`/`exercises` arrays are empty. Authoring is therefore string generation, and
`push` only has to split on `# Week` / `## Day` headers.

### Results store: append-only JSONL, not SQLite
**Ruling.** `snapshot` writes a verbatim raw JSON snapshot, a canonical `history.jsonl` upserted by
workout id, and a flattened `completed_sets.jsonl` regenerated from it. All under `data/`, gitignored.
**Why.** The pattern is borrowed from Dogsheep (`<service>-to-sqlite` + `sqlite-utils`), whose good
idea is idempotent upsert by primary key, not the storage engine. At this scale — hundreds of
workouts, tens of thousands of sets — a query engine buys nothing that a `json.loads` per line
doesn't, and JSONL stays diffable, greppable, and readable without a tool. The raw snapshot is kept
separately so a parsing bug is always recoverable: re-derive, never re-fetch.
**The flattening is the actual safety feature.** Every Liftosaur set carries both planned
(`reps`/`weight`/`rpe`) and performed (`completedReps`/…) values, gated by `isCompleted`. Reading
the planned fields yields numbers that look like results and are not. `completed_sets.jsonl` makes
that mistake unavailable to analysis code.
**Reopens if.** Cross-era queries get painful enough to want SQL, at which point the JSONL loads
into SQLite in one command anyway.

### Hevy history archived and analysed, not imported into Liftosaur
**Ruling.** Keep the Hevy export in `data/hevy/` and the derived findings in `history.md`. Do not
run Liftosaur's native Hevy CSV import.
**Why.** The import (`src/utils/importFromHevy.ts`) maps names through a 259-entry table, dedupes by
start time and is undoable — it works fine. But it carries no RPE (Hevy's column is empty across all
1236 rows anyway), and it would put 64 sessions of six-to-nine-month-old, partly-substituted
exercise data into the same account the weekly review reads from. The history's real value is a
sanity check on starting loads, and `history.md` delivers that without polluting the signal.
**Reopens if.** A cross-era progression chart is wanted badly enough to accept the noise.

---

## Program

### Return-to-training ramp: 1 week, not 3 — with one exception
**Ruling.** One week at 2 sets/RIR 4, then the program as written. Romanian deadlift alone keeps
the 3-week ramp.
**Why.** The tendon-lag mechanism supports having a ramp; nothing ever measured its *duration*.
No trial randomizes ramp length in returning lifters and reports injury rates. Three weeks was
convention, and this document's whole method is refusing convention where nothing measured it.
The RDL is excepted because loaded lumbar flexion at a long muscle length is the highest-
consequence failure mode in the program — the ramp is a property of the lift, not the calendar.
**Reopens if.** New joint or tendon pain persisting >48 h, or a sharp drop in a lift's rep quality
at unchanged load. That triggers a per-lift back-off of ~15% and a two-week re-ramp, not a
program-wide reset.

### Rest intervals are the duration lever; warmup configuration is not
**Ruling.** Per-line rest timers: 120 s compounds, 75 s isolation. Calf raise left at the global
default.
**Why.** Measured, not reasoned. Adding `warmup: none` across the program moved the app's duration
estimate by exactly zero, confirmed after save, after reload, and from a fresh share link, while a
control change did move it. Rest timers moved it 330 → 253 min/week. An earlier additive model
(`warmup×90s + working×180s`) reproduced 80–90% of the app's figures and was retracted once tested
directly — it was curve-fitting, not mechanism. **We still do not know Liftosaur's duration
formula**, and the app's estimate is not a measurement of this program. Time a real session.
**Calf raise exception.** Its myo-rep protocol needs 15–20 s between mini-sets, which isn't
expressible as set groups. A uniform 75 s would fight the intended structure, so nothing was
encoded rather than encoding something wrong.
**Reopens if.** A timed real session lands far from 253 min/week either way. Sessions are still
well over the 32–38 min target — Day 1 by ~30 min — and pushing rest lower trades against load
protection. Undecided.

### Dumbbell weights are per dumbbell, and Hevy's are not
**Ruling.** `program.liftoscript` states the weight of **one** dumbbell. Hevy's export states the
**combined** weight, so every historical dumbbell number is halved on the way in.
**Why.** Liftosaur's `dumbbell` equipment has `multiplier: 2` and a 10 lb bar — structurally
identical to `barbell` (multiplier 2, 45 lb bar), where the multiplier is the two loadable sides of
one implement. Hevy's convention isn't declared anywhere in the export, so it was settled by three
independent consistency checks against barbell lifts logged in the same sessions; all three agree
on "combined". Full working in `history.md`.
**Reopens if.** A logged session comes back at half or double the expected load — that is what
getting this backwards looks like, and it is self-announcing.

### Progression increments are per-hand, so small lifts get 2.5 lb
**Ruling.** Dumbbell upper-body and isolation lifts progress by `dp(2.5lb)`. Bulgarian split squat
keeps `dp(5lb)`. Barbell, cable and machine lifts are unchanged.
**Why.** Invisible until real loads were written in: `dp(5lb)` on a dumbbell lift is 5 lb *per hand*,
which is +40% on a lateral raise and +25% on a curl. The history shows that exact failure — lateral
raises pinned at 30 lb total for six months with reps declining 12 → 10 → 8, which is what an
unreachable next increment looks like from the inside. The gym has 2.5 lb dumbbell steps (visible in
the logged weight ladder), so the finer increment is actually available.
**Reopens if.** A lift clears its rep ceiling on all sets two sessions running — then the increment
is too small and is costing time.

### Judge progress by the logbook, not by scans
**Ruling.** Eight weeks of logged progression decides whether the program works. InBody scans are
trend-only, every 8–12 weeks.
**Why.** At realistic gain rates, scan noise exceeds signal. See `scans/scans.md` for the
derivation-chain audit and `abs.md` for why no device-derived body-fat percentage is trustworthy
here in either direction.

### Cycling is the default cardio slot, not swimming
**Ruling.** If one cardio modality happens, it is cycling. `swimming.md`'s analysis stands on its
own terms and is not withdrawn — swimming simply loses the head-to-head for *this* lifter.
**Why.** Both are near-zero-interference for the lower body (Wilson 2012: running interferes,
cycling doesn't; swimming sits with cycling as non-weight-bearing). They separate on the risk
column, not the benefit column. Swimming's real cost is upper-body specific — pull-dominant
fatigue competing with rows and pulldowns, and shoulder overuse sharing the exact tissue pathway
as incline press, flat press/dip and lat pulldown (`swimming.md` §§1–2). Cycling is lower-body,
so it touches neither, and it adds no wrist load beyond light handlebar grip, which matters given
the rehabbed right wrist plus recurring squash load on the same side (`CLAUDE.md`, Injuries).
Swimming also needs 8–12 weeks of technique work before it reaches a real training zone; cycling
delivers 235–283 kcal and a genuine aerobic stimulus from the first session.
**Reopens if.** A pool becomes dramatically more convenient than a bike route (adherence beats
optimality — `exercises.md`, "What optimal means"), or a knee/road-safety issue makes city riding
unattractive. Note the two are not exclusive; this ruling only settles which one gets the slot
when only one will realistically happen.

---

## Open, not yet decided

- **Whether to buy a Liftosaur subscription** for `run_playground` and `get_program_stats`.
- **Whether to cut rest intervals further** to reach the 32–38 min/session target, against load
  protection.
- **Whether to keep `Claude-Session` links in commit messages** once the repo is public — they are
  in all commits to date. See `PUBLISHING.md`.
