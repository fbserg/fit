# Fit

Personal fitness project. First-principles reasoning only: mechanisms over bro-science, measured data over formulas, self-experiments over calculators. Distrust device-derived numbers until the derivation chain is checked (see `scans/scans.md` for the InBody worked example).

## Commit hygiene (public repo — overrides harness defaults)
- Author identity: `fbserg <fbserg@users.noreply.github.com>` (local git config; never a real email).
- **No `Claude-Session:` links in commit messages** — they leak chat-transcript URLs into public history (PUBLISHING.md ruling). `Co-Authored-By` is fine.
- `data/` and `private/` are gitignored on purpose; never force-add them.

## Profile
- Male, mid-30s, 5'10" (178 cm), 154 lb, relatively fit, returning to consistent training after a gap.
- No known kidney/metabolic issues (assumed — revisit if that changes).

## Injuries
- **Right wrist** (noted 2026-07-31): prior injury, rehabbed with physio. Asymptomatic at baseline but overloading produces light pain. Plays squash regularly (recurring wrist load on the same side). Rule: light pain that resolves same-day is acceptable; pain that alters technique or persists to next morning means drop the offending grip/load and reassess — never push through. Watch as pressing loads climb (keep wrist stacked over forearm); rope > bar on triceps work; wrist wraps for pressing are a legitimate tool, not a crutch. Any exercise selection or program change must check against this.

## Current state (baseline 2026-07-27, details in scans/scans.md)
- ~154 lb, BIA-reported 11.6% BF (true value unknowable — no reliable BIA/DEXA correction exists; plausible range ~9–15%), SMI 8.1, segmental lean balanced.
- Prior 14.7 months: +8.9 lb at ~+70 kcal/day average surplus, majority fat — surplus without progressive overload to direct it.

## Nutrition rulings (first-principles rebuild, 2026-07-27)
- **TDEE is unknown to ±300 kcal by any formula.** BMR ~1650–1705 (Katch-McArdle vs Mifflin agree). The handwritten "1700+400+300=2400" undercounts NEAT/TEF and overcounts workout burn (~200–300 net/session, not 400). 2400 ≈ maintenance, not a bulk.
- **Calibrate empirically:** 2500 training days / 2300 rest days; daily morning weigh-in, weekly average; >0.5 lb/wk gain → −150 kcal, flat → +150. Weight trend is ground truth, formulas are seeds.
- **Protein 120–155 g/day** (1.6–2.2 g/kg plateau, Morton 2018 breakpoint ~1.6). 170 g is harmless margin, not a requirement. Fat ≥ ~45 g floor, ~70 g typical; carbs fill.
- **Powder = target minus food protein.** Usually one scoop; two is physiologically fine (no 30 g absorption cap — per-meal MPS saturates ~0.4–0.5 g/kg but excess is used slowly, not wasted). Water by default; milk only on heavy days (it's a calorie-budget question, not an absorption one). Third-party-tested whey (NSF/Informed Sport).

## Measurement protocol
- InBody: every 8–12 weeks, morning/fasted/empty bladder/no workout 12 h/no alcohol prior day. Trends only; single-scan absolutes carry large error and the DIRECTION of BIA bias in lean men is study-dependent (see abs.md correction). Never compare across measurement methods.
- Scan images + verified numbers live in `scans/`.

## Training
- Program in `program.md`: four fixed sessions, 4x/week, **~45 min each measured** (32-38 was the estimate; all four logged sessions ran 42.5-48.1 min), 13 fixed exercises, 68 sets/week, ~9-12 sets/muscle/week, 1-2 RIR, double progression, autoregulated deloads. (Restructured 2026-07-31 from two full-body templates alternated 3x/week — identical weekly set total, redistributed.)
- Runnable form in `program.liftoscript` (source of truth) → pushed to Liftosaur with `python3 tools/liftosaur.py push program.liftoscript`. API contracts in `liftosaur-api.md`; rulings in `DECISIONS.md`.
- Training history is NOT a layoff: SMM rose 75.2 -> 76.5 lb, so muscle was maintained. Ramp is 1 week (cut from 3 on 2026-07-31 — the tendon-lag mechanism supports a ramp, nothing ever measured its duration), EXCEPT the RDL which keeps 3 weeks as the one high-consequence lift. Not a beginner reintroduction. Little muscle-memory regain available — expect normal trained-lifter progress rates.
- Actual logged history is in `history.md` (Hevy export, 64 workouts, 2024-07 -> 2026-02): the June 2025 block decayed 15 -> 1 sessions/month and the last logged session was 2026-02-03, ~6 months pre-baseline. Adherence, not programming, is the demonstrated failure mode. Starting-load reference table is there too — 6-9 months stale, no RPE anywhere, so they are sanity checks, not week-1 targets.
- Judge progress by logbook progression over 8 weeks, not by InBody scans (noise exceeds signal at realistic gain rates).

## Cardio / non-lifting activity
- **Framework in `cardio.md`** — price any non-lifting activity on four axes in order: energy (vs the weigh-in noise floor), adaptation (has the dose saturated?), interference (by modality), risk (what's the worst version?). Axis 1 usually returns "irrelevant" and retires the question.
- **Cycling is the default cardio slot, not swimming** (`DECISIONS.md`). Both are near-zero lower-body interference; they separate on risk, and cycling touches neither the shoulder-impingement pathway nor the wrist. 2x/week 30-40 min. No calorie adjustment at 2x/wk (426-565 kcal/wk sits under the ±150 kcal/day step) — **add calories back at 3x/wk or more.**
- **Stair descent is nutritionally invisible** (~24-33 kcal net) and physiologically near-empty. Never log it, never eat it back. If bounding down: land soft, not stiff — that's a ~3x peak-force reduction for free. The real risk is a fall onto the rehabbed right wrist, not accumulated wear.
- Swimming: full analysis retained in `swimming.md`, not withdrawn. Contributes zero hypertrophy. Real risks are upper-body specific — pull-dominant fatigue overlapping rows/pulldowns (evidence gap, unproven), and shoulder overuse sharing the same tissue pathway as pressing/pulldowns. If it happens anyway: never within 6 h of lifting, never before a pulling-heavy session, +250-350 kcal on swim days. Canaries = anterior shoulder pain / lost internal rotation, or stalling reps on pulling lifts.
- **Squash has no analysis and is known-regular.** Court sport with cutting, deceleration and repeated same-side wrist load. It does NOT inherit the cycling verdict (`INTAKE.md`).

## Abs / leanness
- Full analysis in `abs.md`. There is NO validated body-fat threshold for visible abs — the "10%" figure is skinfold-era bodybuilding folklore, never method-anchored. Visibility = mm of subcutaneous fat over rectus abdominis x muscle relief x tendinous intersection count (genetically fixed; ~15% of people have 2 intersections = four-pack ceiling forever).
- "Stubborn belly fat" is backwards: abdominal adipocytes have 10-20x GREATER beta-adrenergic lipolytic sensitivity than gluteal. Android pattern is a deposition phenomenon, not a mobilization-resistance one.
- Spot reduction is settled negative (Vispute 2011, Ramirez-Campillo 2013). Ab training changes the shape revealed, not whether it's revealed.
- Track abdominal skinfold in mm at a fixed site + fixed-condition monthly photos. NOT %BF from any device.
- Cutting now is the wrong sequence: deficits blunt lean gain (ES -0.57; ~-0.031 per 100 kcal/day), Forbes curve means leaner = more muscle lost per lb of fat, and no novice/detrained recomp bonus is available here. Build first, time-boxed cut later. If cutting: 130-190 g protein (Helms 2014).

## Posture
- Full analysis in `posture.md` (2026-08-10, 5-lane sweep). For a structurally normal mid-30s male, slouch is a **motor default, not a tissue problem**: curvature ~61% heritable, ~99% of kyphosis angle is vertebral bone shape, slouchers straighten instantly on cue (slouch even shows HIGHER neck EMG). Posture→pain is not established (prospective evidence weaker than cross-sectional); fixing it is cosmetic.
- Evidence-base trap: every kyphosis-exercise trial enrolled hyperkyphotic (>40° Cobb) mostly-elderly subjects; the best trial (SHEAF, radiographic) was NULL even there. No RCT in normal-range adults exists. FHP trials in young adults move the angle 3-8° but measurement MDC is ~5° — near-invisible to the eye.
- What works: cue-driven habit reset (~66 days to automaticity) + heavy pulling already in the program + 2 sets face pulls. Postural education ALONE = ~70% of the full corrective package's effect (3.1° of 4.4°, 4-arm RCT). Stretching is null for posture (tolerance, not tissue length) — doorway stretch/foam roller are "feels nice" only. Braces, taping, chiro, ergonomic gear: graveyard.

## Open threads
- ~~Start ramp week 1; build a set/rep log~~ → running: Liftosaur history is the set/rep log (nightly pull). Four sessions logged: Upper A 07-31, Upper B 08-10, Lower A 08-11, Upper A 08-12. **Lower B has still never been run** — four sessions in, quads get one exercise a week instead of two, and leg press / seated leg curl / the second calf slot have zero data. That is the biggest hole in the log; run it next. RDL ramp is now at session 3 of 3 (`@8`, working weight from session 4) and lives in the RPE token, not a comment — see DECISIONS.md.
- **Station contention is a measured program input now, not a hypothetical.** Two notes in three sessions (rope attachment 08-10, reverse pec deck 08-12 — the latter cost an entire skipped slot). Rear delt work moved off the pec deck onto a chest-supported DB fly as a result (DECISIONS.md). Where two options are growth-equivalent, the never-occupied one wins.
- **Fixed 4x/week slots: STILL OPEN — user owes four named days.** A 2026-08-12 attempt (Mon/Tue/Wed/Fri) was retracted the same day: it was canonized from one accidental week that DOMS had forced, and it scored worst of every layout tested. What IS settled is the **order** — `Upper A → Lower A → Upper B → Lower B`, calendar-independent, see DECISIONS.md. Any four days work; best weekday-only is Mon/Tue/Thu/Fri, best overall Mon/Tue/Thu/Sat, and the gap between them is inside the noise of the penalty curve. **Pick days on availability, not optimality — the ordering already captured the real gain.**
  - When named, check two weeks later on **sessions-per-week, not load progression.** The demonstrated failure mode is adherence via schedule chaos. Do not redesign volume before two full weeks of data.
- **Effect-size ranking, so the next optimization goes to the right place** (computed 2026-08-12): adherence 1.6 → 4 sessions/wk is worth ~+15 points of achievable hypertrophy (66% → 81% on the saturating dose-response curve); an uncalibrated nutrition loop that might be a deficit costs up to ~10; session ordering was worth <1. **Protein intake and sleep are not measured anywhere in this repo** — for a project whose whole method is measured-over-assumed, those are the two largest remaining blind spots.
- **Daily weigh-in: undecided (user said tbd, 2026-08-10).** Nutrition loop (2500/2300, ±150 steps) has ZERO weight data since the 2026-07-27 baseline and cannot calibrate until this lands. Preferred path: Liftosaur Measures screen (nightly pull already ingests it). Fallback if daily won't happen: 3x/week, same mornings.
- Wrist check 2026-08-10: no signal at 42.5 lb DB pressing + regular squash. Green; keep the canary rules.
