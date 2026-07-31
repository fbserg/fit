# Fit

Personal fitness project. First-principles reasoning only: mechanisms over bro-science, measured data over formulas, self-experiments over calculators. Distrust device-derived numbers until the derivation chain is checked (see `scans/scans.md` for the InBody worked example).

## Profile
- Male, mid-30s, 5'10" (178 cm), 154 lb, relatively fit, returning to consistent training after a gap.
- No known kidney/metabolic issues (assumed — revisit if that changes).

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
- Program in `program.md`: four fixed sessions, 4x/week, ~32-38 min each, 13 fixed exercises, 68 sets/week, ~9-12 sets/muscle/week, 1-2 RIR, double progression, autoregulated deloads. (Restructured 2026-07-31 from two full-body templates alternated 3x/week — identical weekly set total, redistributed.)
- Runnable form in `program.liftoscript` (source of truth) → pushed to Liftosaur with `python3 tools/liftosaur.py push program.liftoscript`. API contracts in `liftosaur-api.md`; rulings in `DECISIONS.md`.
- Training history is NOT a layoff: SMM rose 75.2 -> 76.5 lb, so muscle was maintained. Ramp is 1 week (cut from 3 on 2026-07-31 — the tendon-lag mechanism supports a ramp, nothing ever measured its duration), EXCEPT the RDL which keeps 3 weeks as the one high-consequence lift. Not a beginner reintroduction. Little muscle-memory regain available — expect normal trained-lifter progress rates.
- Actual logged history is in `history.md` (Hevy export, 64 workouts, 2024-07 -> 2026-02): the June 2025 block decayed 15 -> 1 sessions/month and the last logged session was 2026-02-03, ~6 months pre-baseline. Adherence, not programming, is the demonstrated failure mode. Starting-load reference table is there too — 6-9 months stale, no RPE anywhere, so they are sanity checks, not week-1 targets.
- Judge progress by logbook progression over 8 weeks, not by InBody scans (noise exceeds signal at realistic gain rates).

## Cardio / swimming
- Full analysis in `swimming.md`. Verdict: no meaningful interference with hypertrophy (interference is driven by eccentric damage from running, not aerobic work per se; swimming is non-weight-bearing). Contributes zero hypertrophy — it's cardio/VO2max/longevity only.
- Real risks are upper-body specific: pull-dominant fatigue overlapping rows/pulldowns (evidence gap, unproven), and shoulder overuse sharing the same tissue pathway as pressing/pulldowns.
- If added: 2x/week 30-40 min, never within 6 h of lifting, never before a pulling-heavy session, +250-350 kcal on swim days. Canaries = anterior shoulder pain / lost internal rotation, or stalling reps on pulling lifts.

## Abs / leanness
- Full analysis in `abs.md`. There is NO validated body-fat threshold for visible abs — the "10%" figure is skinfold-era bodybuilding folklore, never method-anchored. Visibility = mm of subcutaneous fat over rectus abdominis x muscle relief x tendinous intersection count (genetically fixed; ~15% of people have 2 intersections = four-pack ceiling forever).
- "Stubborn belly fat" is backwards: abdominal adipocytes have 10-20x GREATER beta-adrenergic lipolytic sensitivity than gluteal. Android pattern is a deposition phenomenon, not a mobilization-resistance one.
- Spot reduction is settled negative (Vispute 2011, Ramirez-Campillo 2013). Ab training changes the shape revealed, not whether it's revealed.
- Track abdominal skinfold in mm at a fixed site + fixed-condition monthly photos. NOT %BF from any device.
- Cutting now is the wrong sequence: deficits blunt lean gain (ES -0.57; ~-0.031 per 100 kcal/day), Forbes curve means leaner = more muscle lost per lb of fat, and no novice/detrained recomp bonus is available here. Build first, time-boxed cut later. If cutting: 130-190 g protein (Helms 2014).

## Open threads
- Start ramp week 1; build a set/rep log.
