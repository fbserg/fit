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
**Reopens if.** Liftoscript stops being able to express something the program needs. The
formerly-known gap — myo-reps — closed 2026-08-10: per-set-group rest timers make the mini-set
structure fully expressible (see the corrected rest-timer ruling below).

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

### The repo is not the source of truth between sessions — pull, merge, push
**Ruling.** `program.liftoscript` is authoritative only at the moment it is pushed. Every edit
after the first logged session must be made on the *live* text pulled from the account, not on the
repo copy, and the repo file is then overwritten with what was pushed. Never push a repo file that
predates a session.
**Why.** Found 2026-08-12, three sessions in. `dp()` does not keep progression in a side table —
it rewrites `exerciseText` in place. After Days 1–3 the live program read
`Romanian Deadlift ... 4x7-10, 1x5-10` and `Bicep Curl / 2x8-12 22.5lb @9+, 1x8-12 20lb @10+`,
neither of which exists in the repo. Liftosaur's dp raises each set's *minimum* to last session's
completed reps + 1 (a beat-last-time target) and advances weight per set index, so state is
per-set and accumulates fast. Pushing the repo file verbatim would have silently reverted every
bit of it. `liftosaur.md`'s "this repo can be the source of truth and the app is just a runner"
was true before any set was logged and false afterwards.
**Reopens if.** Liftosaur adds a progression store separate from the program text, or `push` grows
a merge step that reconciles automatically instead of relying on the operator to pull first.

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
**Amended 2026-08-12 — a ramp described in a comment is not a ramp.** The RDL line read
`5x6-10 95lb @8+` while the comment above it said "weeks 1-3 at RIR 4-3-2". @8 is RIR 2. Session 1
was therefore prescribed at week-3 intensity and trained that way. Comments do not constrain the
app and were never going to; the RPE token is the only thing the lifter is actually shown per set.
The ramp is now encoded in the number — `@7` for session 2, `@8` from session 3 — and the comment
only explains it. Any future ramp must move the token, not the prose.

### Session order alternates upper/lower — and it is a fifth-order variable
**Ruling.** Days run `Upper A → Lower A → Upper B → Lower B`, never in the old numeric order.

**Correction, 2026-08-12 (believed at the time: "named, not renumbered, so history records logged
as 'Day 2' keep meaning what they meant"). That sentence was false.** Comparing
`data/liftosaur/raw/2026-08-12T18-20-57Z.json` against `…18-38-50Z.json`, slots 2 and 3 physically
swapped contents: slot 2's first working line went from `Bench Press, Dumbbell` to
`Romanian Deadlift, Barbell`. The days were renamed *and* reordered. So `history.jsonl`'s
2026-08-10 record carries `day=2` meaning the flat-press day, while every future Lower A record
will carry `day=2` meaning the hinge day. **All analysis must key on `dayName` plus exercise id,
never on the day index.** This is also a standing argument against further slot reordering — every
reorder silently reinterprets the existing log.
**Why.** Enumerated rather than argued. Every muscle appears on exactly two days, and the day-pairs
are (1,2)×3 — chest, lats, side delts, 26 sets — and (3,4)×2 — hamstrings, quads, 18 sets. Numeric
order collides both of the big ones; alternating collides only the 5–9-set arm and calf pairs.
Averaged over all 35 possible four-day weekday patterns: `1-2-3-4` scores 41.7, `1-3-2-4` and
`1-4-2-3` both score 20.8 and are exactly symmetric. The finding is calendar-independent, which is
why it shipped before the calendar was settled. Stable under four different fatigue-penalty curves
and not driven by the hamstring risk multiplier (40.6 → 37.9 with it removed).
**The honest size of this.** The score measures acute force decrement on the second exposure, and
that does *not* convert cleanly into hypertrophy: at a fixed RIR target a fatigued muscle simply
reaches that RIR at fewer reps, and the set still counts as a hard set — hard sets are the dose
variable, volume-load is not. The real payoff is a clean progression signal, since double
progression reads fatigue-induced rep loss as failure-to-progress and stalls the load for the
wrong reason. Worth <1 point of achievable hypertrophy against ~15 for fixing adherence. It shipped
because it was free, not because it mattered.
**What this corrects.** The 2026-08-12 slot ruling picked numeric order *because it made the app's
`nextDay` self-serve*, then defended it with "adherence beats optimality" — invoking a real
principle as a trump card without pricing either side, which is the exact move this document
exists to refuse. The friction was also fake: renaming the days removes it entirely.
**Reopens if.** The program's exercise-to-day assignment changes, which would redraw the pair table.

### The squash restructure is refused — the premise that forced it was false
**Ruling.** Thursday squash changes **nothing structural**. The four templates stay byte for byte.
Squash is handled by a calendar phase that already exists, one execution rule, and one calorie
recode. Specifically: `Mon Upper A · Tue Lower A · Wed Upper B · Thu squash · Fri Lower B`, which
is the phase the `nextDay` pointer lands on for free once Lower B is run.

**What was proposed and rejected.** Splitting the lower work by muscle (posterior Monday, anterior
Tuesday) and moving both lower days to Mon+Tue, so no lower session sat adjacent to Thursday.
Same 13 exercises, same 68 sets, all nine weekly targets met — the arithmetic was correct and
verified independently. It fails on premise and on distribution, not on bookkeeping.

**Why.** Three findings, in descending order of force. Established by a five-lens adversarial
panel plus two competing blank-sheet designs and a judge, 2026-08-12.

1. **"No arrangement of the current templates satisfies the constraint" is false by enumeration.**
   Of the 24 assignments of the four templates to Mon/Tue/Wed/Fri, four put both lower days on
   Mon+Tue with zero template edits. The rebuild was justified by needing to spend the
   upper/lower alternation ruling — but spending that ruling *alone* was sufficient. The argument
   contradicted itself: it paid twice for something available once.
2. **The load-bearing number — a "48–72 h" isolation window — has no source.** Not in this repo
   (`data/` holds zero squash sessions, zero HR, zero duration, zero soreness) and not in the
   literature: the only systematic review of racket-sport physiological demands found no squash
   studies at all and reports no muscle-damage marker for any racket sport. The nearest measured
   analogue runs the other way — a 3-hour simulated tennis match dropped 1RM squat 35% immediately
   post-match, with strength and jump height **not significantly different from baseline at 24 h**
   ("mild muscle damage"). One weekly recreational game in a habituated, resistance-trained player
   sits at the damage floor twice over: the repeated-bout effect never lapses at weekly intervals,
   and resistance training already confers the adaptation. `cardio.md` mandates pricing energy
   cost *first*; that axis was skipped entirely and axes 3–4 were run by assertion.
   *This is a PLAYBOOK rule-16 violation: a C-tier recalled number made load-bearing without
   derivation, two weeks before the instrument that would measure it ships.*
3. **The distribution moves the wrong way on the one axis that matters.** Under the current
   templates each lower day carries both quads and hams, so a missed session still delivers 4–5
   of each. Under the proposal a missed Monday **zeroes** hamstrings and a missed Tuesday zeroes
   quads. At an observed completion rate below 1.0, concentrating a muscle into a single weekly
   session is strictly worse — and adherence is the ~15-point variable while layout is the
   <1-point one. `program.md` line 18 says frequency's "only real benefit is indirect: spreading
   sets prevents junk volume late in a session"; the proposal cited the first half of that
   sentence to license violating the second.

**What survives from it.** Nothing structural. The day-*before* half of the squash concern is
retained as a **squash-performance preference, not injury prevention** — the chosen phase puts an
upper day before Thursday anyway, so it costs nothing. The day-*after* half is dropped outright:
Lower B is all-machine, no balance demand, and the lightest wrist day in the program, which makes
it the *right* session to run after a court sport rather than the wrong one.

**The diagnosis was also weaker than it looked.** "He picks the session on arrival and the leg day
loses" rests on n=1, with a confound this project caused: between the 18:20 and 18:38 snapshots on
2026-08-12 the day list was renamed *and* slots 2/3 swapped contents. He opened, 58 minutes later,
an app whose day list had just been rewritten with names he had never seen, and started at the top.
`nextDay` read 4 (Leg Press) throughout. That is a further reason not to rebuild templates on it —
and no reason at all not to ship the free execution rule.

**Honest effect size.** The whole layout question is worth 1–3 points of achievable hypertrophy,
most of that being "do not concentrate a muscle into one session" rather than "pick this weekday."
The execution rule below sits on the ~15-point adherence axis and costs one sentence. Recoding
Thursday's calories sits on the ~10-point nutrition axis and costs nothing. Protein, sleep, and a
weigh-in loop with zero data points 16 days after baseline remain untouched by any of this.
**The correct amount of further effort to spend on where the leg press goes is zero until
2026-08-30.**

**Reopens if.** Lower B is skipped again in the two-week window (Mon 2026-08-17 → Sun 2026-08-30)
*with the pointer bound and no rename confound*. Then the answer is the blank-sheet alternative —
four mixed sessions, one lower compound each, every muscle 2×/week, zero adjacent-day collisions
(arithmetic already verified: 14+19+16+19 = 68, all nine targets exact). Adopt it then, not now.
Also reopens if measured squash data (duration + HR + next-morning soreness, 3–4 sessions) shows
real next-day impairment — which is what `tools/health_connect.py` was built to capture.

### The app's pointer is the session — no picking on arrival
**Ruling.** Whatever `nextDay` offers when you open the app **is** the workout. The only legal
deviation is a logged note saying why. Bind the *calendar* (Mon/Tue/Wed/Fri, same time); let the
app bind the *content*. A missed session is not made up and does not re-anchor — the pointer keeps
its order and the weekday mapping rotates by one.
**Why.** The rotation is the feature. It is what makes it structurally impossible for any one
template to be systematically starved, which is exactly what self-selection did to Lower B for
four sessions. This is the whole intervention that the restructure was trying and failing to buy
with geometry: no template arrangement can fix a tap. It sits on the ~15-point adherence axis and
costs one sentence.
**One override, once.** Friday 2026-08-14: the pointer reads 2 (Lower A). Override to Lower B. That
gives Lower B its first-ever run, closes the week at eight of nine muscle targets, and advances the
pointer 4 → 1 so Monday starts the recurring phase with no further override ever needed.
**Reopens if.** Sessions-per-week does not improve over Mon 2026-08-17 → Sun 2026-08-30. Judge on
sessions-per-week, **not** load progression, and do not touch volume or templates before 08-30.

### Straps on the Romanian deadlift, from session 2 on
**Ruling.** Straps for every RDL working set. Not for anything else. **Amended same day — the
lifter does not own straps, so the ruling ships with a fallback ladder:** chalk (fixes bar slip,
which was the acute failure, but not forearm fatigue) → stop at 4 sets rather than grind a
grip-limited fifth → trap bar if available → 45° back extension holding a plate, which is the only
option that removes grip entirely. Buying straps is still the answer; the ladder exists so the
program never instructs equipment the lifter doesn't have.
**Why.** Session 1 (2026-08-11) ended on grip: forearm pump, the fifth set fell to 4 reps because
the bar slipped, and the lifter's own note put back and legs at "regular tired" — 90 lb on a lift
whose Hevy history shows 115 × 8. Grip endurance is the binding constraint and it is not a target
of this program, so it was capping the hamstring stimulus for nothing. Straps also remove bar load
from the rehabbed right wrist, which is free upside given recurring squash load on the same side.
Mixed grip was rejected (asymmetric spinal loading on the one lift where lumbar position is the
whole safety case) and so was hook grip (pain, for a benefit nobody wants here).
**Note the interaction.** Grip failure was acting as an accidental governor — the logged @8 was
grip RPE, so the hamstrings likely got something near the RIR 4 the ramp actually wanted. Removing
the governor without lowering the RPE target would have raised true hamstring load in one step.
That is why straps and the `@7` amendment above ship together.
**Reopens if.** Wrist pain appears under a strapped bar (which would mean the load, not the grip,
was the problem), or grip becomes a stated goal.

### Rear delt fly moves off the pec deck and onto a bench, because availability beat the resistance curve
**Ruling.** Both rear-delt slots (1-3a Upper A, 4-3 Lower B) run **chest-supported DB reverse fly**
— face-down on a 30–45° incline bench at the DB rack — starting at 10 lb/hand, `dp(2.5lb, 12, 20)`,
one shared progression line. Reverse pec deck is demoted to named substitute: use it on the days it
is free, log it on the same line.
**Why.** On 2026-08-12 the pec deck was occupied and all three sets were skipped — the session
delivered zero rear delt work. The lifter's own read was "nice but very busy." Rear delts are the
program's least well-dosed muscle at ~5 direct sets/wk against a 10–14 target (`exercises.md`), so
they are the single worst slot to hang on a coin-flip station. The July ruling that picked the
machine argued the DB version's hip-hinge hold was technique-sensitive for no offsetting benefit.
That was true of the *standing bent-over* DB fly and it quietly assumed that was the only DB
version — an incline bench holds the torso angle and deletes the hinge hold outright, so the one
named sacrifice does not exist in the version now prescribed. The machine's surviving edge was
cleaner increments; the pin stack steps 10 lb and dumbbells step 2.5 lb, so it loses that too.
Bonus, not the reason: 1-3a/1-3b now both live at the DB rack, collapsing a two-station superset to
one and retiring the "is it rude to hold both?" question for that pair.
**The general form, which is the part worth keeping.** *A slot's exercise choice is only as good as
the station's availability, and availability is measured, not assumed.* This gym has now produced
two contention notes in three sessions (the rope attachment on 2026-08-10, the pec deck on
2026-08-12). Where two options are growth-equivalent, the one that is never occupied wins, and
"growth-equivalent" is doing no work in that sentence — a skipped set scores zero on every
criterion.
**Reopens if.** DB reps stall while the rear delts still feel short of failure, or trap/upper-back
compensation shows up despite the bench — then back to the machine, accepting the availability risk.

### Stop at the top of the rep range — overshooting reps costs progression
**Ruling.** When a set reaches the printed maximum, rack it. Do not keep going because reps are
available.
**Why.** Mechanical, not philosophical. Liftosaur's `dp` raises each set's next-session minimum to
completed reps + 1, **capped at the range maximum** (`liftosaur.md`). Reps past the cap therefore
buy exactly nothing toward progression while spending fatigue that lands on the later sets of the
same exercise. 2026-08-12 incline press is the worked example: 12, 12, 9, 10, 9 at 37.5 lb in a
6–10 range. The two 12s were four wasted reps, and sets 3 and 5 came in under 10 — so the load
increase did not trigger. Capping the first two sets at 10 plausibly makes all five 10s and moves
the lift to 40 lb. Overshoot at low RPE is not a free bonus; it is a signal the load is too light,
and the fix is the next dumbbell, not more reps.
**Reopens if.** The rep-cap mechanic changes (it is app behavior, verified 2026-08-12, not theory).

### Rest intervals are the duration lever; warmup configuration is not
**Ruling.** Per-line rest timers: 120 s compounds, 75 s isolation. Calf raise left at the global
default.
**Why.** Measured, not reasoned. Adding `warmup: none` across the program moved the app's duration
estimate by exactly zero, confirmed after save, after reload, and from a fresh share link, while a
control change did move it. Rest timers moved it 330 → 253 min/week. An earlier additive model
(`warmup×90s + working×180s`) reproduced 80–90% of the app's figures and was retracted once tested
directly — it was curve-fitting, not mechanism. **We still do not know Liftosaur's duration
formula**, and the app's estimate is not a measurement of this program. Time a real session.
**Calf raise exception — OVERTURNED 2026-08-10.** The original ruling ("myo-reps aren't
expressible as set groups; encode nothing rather than something wrong") failed its first contact
with a real session: the first logged Day 2 showed the app presenting 5 plain sets with the 180 s
global default while every other exercise ran explicit 75/120 s timers, and the lifter — 
reasonably — did 5 heavy straight sets pyramiding 140→200 lb ×8, neither myo-reps nor the 12–15
range. "Encode nothing" turned out to be the *most* wrong encoding available. The factual premise
was also false: timers are per set group, and Liftosaur's own docs cite myo-reps as the intended
use ("this is how you could do myo-reps"). Now encoded as
`1x12-15 @7+ 20s, 4x3-5 @10+ 20s` (3 mini-sets on Day 4) with a `custom()` progression that adds
10 lb when the activation set hits 15 — `dp()` would have gated on the 3–5-rep mini-sets and
never fired.
**Reopens if.** The app renders the custom() progression as a syntax error, or a timed real
session lands far from 253 min/week either way. Sessions are still well over the 32–38 min
target — Day 1 by ~30 min — and pushing rest lower trades against load protection. Undecided.

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
