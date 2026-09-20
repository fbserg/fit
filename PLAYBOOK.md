# Playbook

## What this is

This repo is not a program to copy. Copying the 13 exercises, the set/rep numbers, or the
2400 kcal target transfers none of the value and inherits someone else's constraints (his
gym, his training age, his joints, his schedule). What transfers is the **procedure**: how
to take published dose-response literature plus your own measured data and derive a
program, a nutrition target, and a measurement protocol that are actually yours.

The repo is a worked example of that procedure, with every wrong turn left visible instead
of edited out. The corrections (`abs.md`'s retracted BIA-bias claim, `scans/scans.md`'s
"CORRECTED" note, `exercises.md`'s Refuted section) are the most useful parts — they show
the method catching its own errors, which is the whole point of running it adversarially.

## The method

1. **Separate measured from derived, for every device and every formula.**
   Any instrument gives you raw signal (weight, impedance, a stopwatch split) and a
   formula-derived output (body fat %, VO2max, TDEE). Trace every derived number back to
   its inputs before you trust it as an absolute.
   *Decision rule:* if you can't state the formula, treat the number as trend-only, never
   an absolute. `scans/scans.md` is the worked example — only weight and 10 impedance
   readings are measured; lean mass, fat %, and BMR are all downstream regression outputs.

2. **Before applying a "correction" to a device number, check whether the correction
   itself has consensus.**
   *Decision rule:* if independent sources disagree on the *direction* of a bias (not just
   its size), there is no correction factor. Report a bounded range and stop. `abs.md`
   documents this project retracting its own earlier claim that BIA reads lean men low —
   the literature turned out to disagree on the sign, not just the magnitude, of the bias.

3. **Recompute every term of a formula from its parts before accepting the sum.**
   Handwritten or app-generated TDEE math ("BMR + activity + exercise = target") hides
   double-counts and undercounts. *Decision rule:* itemize each term, check it against a
   published range, and flag double-counted or missing terms explicitly.

4. **Use the formula as a seed, not a target — calibrate against a measured trend with
   pre-committed adjustment rules.**
   *Decision rule:* fix the metric (daily weigh-in, weekly average), fix the trigger
   (e.g. >0.5 lb/wk against goal direction), and fix the adjustment (e.g. ±150 kcal) —
   all three *before* you start, so you're not making the call in the moment you're most
   biased to rationalize it.

5. **Set nutrition/training dose targets from the point where a dose-response curve
   plateaus, not from a memorized per-kg rule of thumb.**
   *Decision rule:* find the study that identifies the breakpoint (e.g. Morton 2018's
   ~1.6 g/kg protein plateau), take a range bounded by it, and stop optimizing past the
   point where more stops helping.

6. **Run a multi-lane adversarial evidence sweep for every major decision, and always
   include a disconfirmation lane whose only job is to argue against the leading answer.**
   Lane names are topic-specific (mechanisms / minimum-effective-dose / practitioner
   convergence / disconfirmation for training; physiology / interference / body
   composition / disconfirmation for cardio) but the shape is fixed: several independent
   lines of evidence, one of them explicitly trying to break the others.
   *Decision rule for resolving conflict between lanes:* RCT/meta-analysis beats expert
   consensus. This project overrode a Delphi-survey consensus on scheduled deloads with an
   RCT showing scheduled deloads hurt strength with no hypertrophy benefit.

7. **Rank candidate variables by effect-size-per-unit-time, and publish an explicit "does
   nothing" list.**
   The ranked-variables list only has value if paired with the null list — otherwise every
   new article about rep range or training frequency reopens a question you already
   settled. Write both down so you stop relitigating it.

8. **Compress time by substitution, not addition.**
   Hold the stimulus (sets, load, proximity to failure) constant and cut the clock —
   supersets, drop sets, rest discipline — rather than adding volume you won't sustain.

9. **Distrust self-report the same way you distrust a device — check it against hard
   data.**
   "About a year off" is a memory, not a measurement. If you have a scan or log spanning
   that period, use it: this project's SMM trend (rising, not falling, across the "layoff")
   overrode a beginner-reintroduction ramp with a much shorter tendon-adaptation ramp.

10. **Select exercises/choices against an explicit weighted-criteria list, with an
    anti-rationalization test for anything you want to cut on "friction."**
    *Decision rule:* would you still drop this if setup/wait/skill cost were zero? If yes,
    it's avoidance, not friction, and it doesn't get to override a stimulus-ranked pick.

11. **Run the adversarial pass as independent drafts that cross-judge each other, and file
    every finding into exactly three buckets: Confirmed, Refuted, Honest uncertainty.**
    Confirmed findings get applied to the main doc. Refuted findings get written down
    anyway — a challenge you considered and beat is worth more than one you never asked.
    Honest uncertainty stays flagged, not silently resolved in whichever direction is more
    convenient.

12. **When you translate the plan into an executable tool, state explicitly which side
    wins whenever the tool's model disagrees with the document's model.**
    A program-tracking app will compute its own per-muscle volume (often via synergist
    credit) that differs from your document's counting convention. Decide in writing which
    number is authoritative before the app's dashboard quietly redefines your targets.

13. **Log corrections in place, labeled with what was believed and why it broke — never
    silently edit a past conclusion out of the document.**
    Every file in this repo does this (`abs.md`'s CORRECTION section, `scans/scans.md`'s
    CORRECTED note, `exercises.md`'s Refuted section). A first-principles document that
    hides its own mistakes is indistinguishable from one that never checked its work.

14. **When data crosses a tool boundary, settle the units by internal consistency — never by
    assumption, and never by reading one number in isolation.**
    Exports rarely declare their convention. This project moved 19 months of history between
    two apps where one logs dumbbells as combined weight and the other as one dumbbell; both
    render as a bare number with `lb` after it, and getting it backwards is a silent 2× error
    in either direction.
    *Decision rule:* find a quantity both tools express and that physiology constrains, then
    check which reading is possible. Here: an incline dumbbell press logged at 80 next to a
    125 barbell bench is only coherent at 40 per hand. Confirm with at least two independent
    pairs before you trust it, and write the ruling down — it will not be obvious again in
    six months.

15. **A progression increment is a percentage, not a number. You cannot choose it until the
    starting load is real.**
    A program written in the abstract can say "add 5 lb" everywhere and look consistent. Once
    actual loads land, the same 5 lb is +5% on a leg press and +40% on a lateral raise, and the
    second one never gets earned.
    *Decision rule:* after seeding loads, compute every increment as a percentage of its own
    starting weight and re-pick anything that lands far outside roughly 2–10%. Check what step
    sizes actually exist on your equipment first — the fix is only available if the rack has it.
    This project's own history shows the failure it prevents: a lift pinned at one weight for
    six months with reps *declining*, which is what an unreachable next step looks like from
    the inside.

16. **Grade every reference number by how directly it measured the thing you're about to do.**
    Old logs are seeds, not targets, and they are not all equally good seeds. Tag each one:
    **A** — same movement, real data. **B** — the movement changed, so a transfer factor now
    dominates the staleness. **C** — no data for this or anything close; it's a guess wearing a
    number's clothes.
    *Decision rule:* say the tier out loud next to the number, and say what would falsify it.
    A C-tier number isn't a problem — pretending it's an A-tier number is. This project's leg
    press seed is explicitly C-tier and expected to be wrong inside the first set, which is a
    fine place for it to be as long as nobody plans around it.

17. **A remembered number is a C-tier number, even when a real citation is attached to it.
    Separate what you remember about *structure* from what you remember about *magnitude and
    direction* — they do not fail at the same rate.**
    `cardio.md` is this repo's cleanest natural experiment on the point, because it was written
    first from recall and then checked line by line. Eight claims needed correcting; two were
    outright backwards. The split was not random:

    | Held up | Needed correcting |
    |---|---|
    | Mechanism claims (eccentric damage drives interference; brief loading is a weak tendon stimulus) | Every specific magnitude (3–3.5× BW, 6–8× BW, 90 m, "descent is ⅓ of ascent", 5–7 MET) |
    | Structural claims (running interferes, cycling doesn't; sustained strain beats fast strain) | Two directions (which way stairs load the kneecap; whether traffic raises or lowers ride intensity) |
    | Anything computed from first principles (mgh framing, impulse–momentum) | — |

    The pattern: remembering *that A exceeds B* is far more reliable than remembering *by how
    much*, and both are more reliable than a number recalled with no derivation behind it.
    *Decision rule:* before any recalled number becomes load-bearing, either derive it or check
    it. Prefer computing to recalling whenever the arithmetic is available — a five-line
    calculation caught three of the eight errors before any literature search ran.

    **The sharpest sub-case, worth its own name: never read a quantity off a correlated proxy.**
    Both backwards claims were this same error. Patellofemoral joint force was inferred from
    ground reaction force — but GRF is higher descending while joint force is higher ascending,
    because the flexion angle at contact changes the quadriceps moment arm. Average ride
    intensity was inferred from the presence of stops — but braking energy has to be regenerated
    on the next acceleration, so stops raise the average rather than diluting it. In both cases
    the proxy is genuinely correlated with the target *and points the wrong way here*. That is
    exactly when the substitution is most tempting and most dangerous. Rule 1's measured-vs-derived
    split catches this when the derivation is explicit; this is the version where the derivation
    is silent and lives only in your head.

## Start here

Minimum path to your own version, in order:

1. Get one real measurement of yourself: at minimum a body weight; ideally a BIA/DEXA scan
   or skinfold readings. You cannot run step 1 of the method on a formula alone.
2. Write your own Profile block (age, height, weight, sex, training history, any relevant
   health flags) — this is the input, not something to copy from here.
3. Apply steps 1-5 to your own scan/food data to get a nutrition target and a calibration
   loop. Do this before touching training — it's the cheaper, faster-feedback half.
4. Apply steps 6-8 to generate a training program: pick variables by evidence rank, run the
   adversarial sweep, publish your own null list.
5. Apply step 10 to select the actual exercises available at *your* gym, with *your*
   schedule tolerance — do not import this repo's 13-exercise list, it was selected against
   one specific gym's equipment and one specific person's stated constraints.
6. Apply step 11 as a second pass over what you just generated: draft independently, cross-
   judge, sort into Confirmed/Refuted/Honest-uncertainty. This is the pass that catches
   arithmetic slips and copy-paste bugs (this repo's arm-volume figure was silently wrong
   until this step caught it) — do not skip it because step 4-5 already "felt" evidence-based.
7. Pick execution tooling (see below) and encode the plan, reconciling the tool's model
   against your document's per step 12.
8. Start training. Judge progress by logbook progression over weeks, not by repeat scans —
   scan noise exceeds real signal at realistic gain rates over short windows.

## Where your answer will differ from mine

| Input that's different for you | What it changes | Don't import this repo's answer if... |
|---|---|---|
| No scan/DEXA/BIA data exists yet | Whether the derivation-chain audit (steps 1-2) applies at all, or you go straight to skinfold + tape + fixed-condition photo trend-tracking | ...you have no scan. Then start with photos/tape, not this repo's %BF numbers. |
| Training age: true novice vs. trained-but-inconsistent vs. long-detrained | Ramp length, whether a fast "muscle-memory" regain window applies, whether simultaneous body-recomposition (losing fat and gaining muscle at once) is realistic at all | ...you're a true novice or meaningfully detrained/higher-body-fat — recomp evidence favors you in ways it does not favor a lean, previously-trained lifter. |
| Session-count / weekly time budget you'll actually sustain | Split structure entirely — frequency and split choice don't move growth at equated volume, so this is pure logistics, not evidence | ...your schedule differs at all. This is the least evidence-constrained, most personal decision in the whole plan. |
| Gym equipment access / crowding | The entire exercise-selection and substitute list | ...you don't lift at a busy commercial gym with the same equipment. Free weights vs. machines, cable vs. dumbbell picks were driven by contention and setup time at one specific gym. |
| Goal: build muscle now vs. cut fat now | Whether the "build first, cut later" sequencing applies, or the opposite (higher-protein deficit) branch does | ...you're not lean/muscle-building-first by choice. A deficit blunts lean gain, so if fat loss is the actual priority the protein target and expected rate both change. |
| Kidney/metabolic health history | Gates the protein ceiling | ...you have any relevant condition. This repo explicitly flags its "no known issues" as an unverified assumption, not a clearance. |
| Willingness to log every set | Whether double-progression/autoregulation works at all | ...you won't track. The entire progressive-overload apparatus assumes a written log; without one you need a cruder, less precise scheme. |

## Traps

What's commonly believed, why it's wrong, and what to do instead. The ones marked *(this
project)* are corrections this repo made to its own earlier conclusions — included because
the self-correction is the demonstration, not something to be embarrassed about.

| Commonly believed | Why it's wrong | Do this instead |
|---|---|---|
| *(this project)* BIA underreads body fat in lean men, so the true number is higher than the device says | Literature disagrees on the *direction* of BIA bias in lean men, not just the size — one line shows overestimation, another underestimation, with 15-20 point limits of agreement | Report a bounded range, trend-only, never cross-method or "corrected" against a different device |
| A handwritten/app TDEE formula ("BMR + activity + exercise") is a valid bulk/cut target | It silently double-counts or undercounts terms — overcounting workout burn, undercounting NEAT/TEF — routinely landing 200-400 kcal off | Itemize every term, treat the sum as a ±300 kcal seed, calibrate against measured weight trend with a pre-committed adjustment rule |
| "10% body fat" is the threshold for visible abs | No peer-reviewed study regresses ab visibility against %BF by any method; the figure is skinfold-era bodybuilding folklore reused across incompatible measurement methods | Track skinfold mm at a fixed site + fixed-condition photos; there is no validated whole-body-%BF threshold to target |
| "Stubborn" belly fat resists mobilization more than other fat | Abdominal adipocytes have 10-20x *greater* lipolytic sensitivity than gluteal — android pattern is a deposition phenomenon, not a mobilization-resistance one | Don't design around a resistance story that runs backwards from the biology; fat-loss rate is systemic, not targetable by location |
| Direct ab work ("free" exercise slotted into a rest window) has no downside | Rectus abdominis is the bracing stabilizer for hinge/squat lifts; pre-fatiguing it in the same session's rest window undermines the lift it's stacked next to, and "zero net time" is false once you account for a third station's setup | Check any "free" addition for hidden interference with the *same session's* primary stimulus before assuming it's free |
| *(this project)* Scheduled deloads on a fixed calendar (e.g. every ~5-6 weeks) improve outcomes, per practitioner-consensus surveys | An RCT inserting a scheduled deload showed it hurt strength with no hypertrophy benefit; expert-consensus surveys are not RCTs and lost the conflict | Autoregulate off actual performance regression, never the calendar |
| A stretched/lengthened joint position automatically means a longer-muscle-length stimulus | Torque from gravity can approach zero exactly at the position assumed to be "long," so the position may not load the muscle there at all; once controlled for loading, no clear hypertrophy advantage remains | Check the torque curve of the actual implement (cable vs. free weight) before assuming a position confers a stretch-bias benefit |
| A first-principles document with citations is self-checking | *(this project)* An arm-volume summary line was silently wrong (copy-pasted from a different muscle's figure) until an independent adversarial audit pass caught it | Recompute totals from source tables during a *separate* audit pass; citations don't protect against arithmetic slips |
| An app's auto-computed stats (e.g. per-muscle set volume) can be trusted as-is | Apps often use a different counting convention (e.g. synergist credit) than your planning document, producing volume numbers that differ by up to 2x for the same session | Decide and state in writing which counting convention is authoritative before the app's dashboard drives a decision |
| Two apps logging the same lift in `lb` mean the same thing by it | *(this project)* Dumbbell weight is combined in one app and per-dumbbell in the other; neither export declares which. Same unit, same number, 2x apart — and it fails silently, because both readings look plausible on the page | Settle it against a quantity both tools express and physiology constrains (a barbell lift logged in the same session), with two independent confirmations, then write the ruling down |
| You can pick progression increments when you write the program | *(this project)* An increment is only meaningful relative to a load. `dp(5lb)` written into an abstract program was +5% on one lift and +40% on another; the +40% one had already stalled for six months in the historical log, reps declining at a fixed weight | Seed real loads first, then re-derive every increment as a % of its own starting weight, bounded by the step sizes your equipment actually has |
| Your old training log tells you where to restart | It tells you where you *stopped* — often already depressed by the decay that ended the block, at an unrecorded proximity to failure, sometimes on a different exercise than the one you're about to do | Discount for time off and for any change in set count per exercise, grade each reference A/B/C by how directly it measured the movement, and let double progression correct you within a few sessions |

## What to build vs. what to install

| Need | Solution | Build or install? |
|---|---|---|
| Program-as-executable-code (progression rules, RIR targets, per-exercise logic) | [Liftosaur](https://www.liftosaur.com/) / Liftoscript | Install — see `liftosaur.md` for a worked encoding, including where the tool's model needed reconciling against the plan's |
| Logging sets in the gym, and progression charting | Liftosaur, Hevy, wger — all of them do this | Install. Never hand-build the phone app or the charts; that is a solved problem and a tar pit. |
| Getting your own logs back out, in a shape you can analyse | A ~150-line script per source | **Build, but keep it thin.** Corrected from an earlier version of this table that said "don't build a logging layer" and read as "don't build anything here." The dashboards are solved; *your specific question* is not. This repo's stall checks need per-set RIR against its own program's rules, which no off-the-shelf chart computes. What to build is only: fetch, archive raw, upsert by primary key, flatten to one row per performed set. Steal the [Dogsheep](https://github.com/dogsheep) pattern (idempotent upsert into a boring local store) and stop there — see `DECISIONS.md`, "Results store". |
| Migrating history between two logging apps | Most apps import each other's CSV natively | Install, but **export and archive first, and read the CSV before importing it.** The import is the last step, not the first. This project's export turned out to have an entirely empty RPE column and a dumbbell-units convention opposite to the destination's — both invisible after an import, both decisive beforehand. |
| Evidence-derived program *generation* — taking dose-response literature and a personal profile and producing an actual program | Nothing off-the-shelf | **Build.** This is the genuine gap. No tool takes published effect sizes and a person's constraints and emits a program; every existing tool assumes you already have the program and just want to execute or log it. The adversarial-sweep-plus-audit procedure in this playbook is the current best answer, not a stopgap for a tool that will show up later. |
| Structured, queryable database of hypertrophy effect sizes across variables | Nothing off-the-shelf | Build if you need it, but check first — reading lists (e.g. Stronger By Science's) exist; a queryable database does not. |
| Stall/plateau detection driving autoregulated deloads | Nothing off-the-shelf found | Build, or apply the decision rule manually against your own log — the rule itself (regression in performance, not a calendar date) is cheap to apply by hand. |

## File map

See `PUBLISHING.md`'s PII table for the full per-item breakdown. At a glance:

| File | Reusable template | Personal-record-only content |
|---|---|---|
| `AGENTS.md` | Methodology paragraphs (nutrition-rebuild logic, protein-plateau logic, measurement-protocol structure) | Profile block, baseline numbers, every kcal/protein figure derived from one person's lean mass |
| `scans/scans.md` | The derivation-chain worked example — reusable near-verbatim, it's method not data | The actual scan values and dates |
| `scans/2026-07-27-inbody270.png` | Nothing — do not use as a template | Entirely personal-record; see `PUBLISHING.md` for disposition |
| `program.md` | Ranked-variable list, null list, time-compression techniques, double-progression rule, autoregulated-deload rule | The 13-exercise list, set/rep tables, the 3-week ramp number (derived from one person's scan) |
| `exercises.md` | The 5-criteria selection framework, the anti-rationalization friction test, the adversarial-pass structure | The friction-audit table (one gym's equipment/crowding), per-exercise picks driven by one person's stated preferences |
| `abs.md` | Nearly the whole document — spot-reduction refutation, tendinous-intersection genetics, deficit-blunts-gains figures are general physiology | Only the closing sequencing call ("build first, cut later") is personal |
| `swimming.md` | Nearly the whole document — interference mechanism, shoulder-overuse literature, prescription numbers transfer directly | The specific fit against one person's lifting split |
| `liftosaur.md` | The encoding methodology (RIR/RPE mapping, per-set-RIR expressibility, app-vs-doc volume reconciliation) | The specific script and exercise-name mapping table (useful as a worked example, not a template to import) |
| `liftosaur-api.md` | Entirely reusable — endpoint contracts with source-line references, the cookie-extraction method, and the four silent-failure traps | Nothing personal; one program id appears as an example |
| `tools/` | Entirely reusable. `doctor`'s check-the-whole-chain-and-name-the-fix structure is the part worth stealing regardless of which app you use | Nothing — the account-specific secret is gitignored, never in the repo |
| `history.md` | The units-trap resolution, the A/B/C reference-grading, and the load-seeding derivation are method | The actual sessions, weights and dates |
| `profile.example.md` | The whole structure — it exists *to be* copied to `profile.md` and filled in | Nothing; the author's filled-in copy is gitignored and never published |
| `INTAKE.md` / `CONFIDENCE.md` / `DECISIONS.md` | All three are structure, reusable near-verbatim: the questions to ask before starting, the weakest-first evidence audit, and the ruling/why/reopens-if ledger format | The specific answers, rankings and rulings |

## Adjusting the program

Cross-references `program.md`, `exercises.md`, `loop.md`, `AGENTS.md`, `abs.md`. Two mechanism/citation errors from an earlier draft of this map are corrected here: the "missed training" rows now cite the tendon-lag mechanism instead of the muscle-*maintenance* curve (a different question — see the note in those rows), and the stalled-single-lift row now cites `loop.md`'s substitution rule instead of `exercises.md`'s friction test (which governs a different kind of complaint). Several `program.md` line citations below were also re-pointed after the 2026-07-31 restructure shifted line numbers.

### The stall-diagnosis order of operations

Getting this order backwards — reaching for exercise selection first — is the single most common failure mode, because churn destroys the clean progression log every earlier step needs (`program.md:158`: "Untracked training cannot progressively overload — this is what makes exercise-churn... actively harmful").

| Step | Check | Rule | Citation |
|---|---|---|---|
| 1 | Adherence/logging | Was every set actually done and logged? Untracked ≠ stalled, it's unmeasured. | `program.md:158`, `loop.md:91` (check 4) |
| 2 | Calories | Weight trend flat 3+ weeks with progression stalling → +150 kcal, not +5 sets | `program.md:192`, `AGENTS.md:15` |
| 3 | Deload trigger | Reps regress at same load across 2 sessions + joints/sleep degrading → 1 wk ~half volume, +3 RIR | `program.md:184-188` |
| 4 | Volume | Only after 1-3 clear: is this muscle actually under its 9-14 set/wk target? | `loop.md:90` (check 3), `program.md:89-100` |
| 5 | Exercise selection | Last resort, single lift only, pre-approved sub table only, and only if the failure meets `loop.md:111`'s evidence-triggered bar (documented pain/joint-comfort issue, not "it's not working" or "variety") | `program.md:122-136`, `loop.md:111`, `exercises.md:11` |

Steps 1-2 are free and non-destructive. Step 5 is the only one that costs measurability — it goes last by construction.

### Situation map

| Situation | Correct knob | Wrong knob (commonly reached for) | Rule / citation | Status |
|---|---|---|---|---|
| **Less time (one bad day)** | Minimum viable session (first pair/exercise, 2 sets, same RIR) or time ceiling (drop last isolation slot at ~45 min) | Rushing rest periods / grinding through at reduced RIR to "fit it all in" | `program.md:149-150` — explicit floor and ceiling rules; RIR is off-limits to convenience | Existing |
| **Less time (permanent, e.g. new job)** | Re-derive session count for the sustainable budget (3x/wk instead of 4x), keeping the *same weekly set total*, since frequency is a null variable | Silently trimming sets below the 9-per-muscle baseline to make sessions shorter — that touches the one variable that's off-limits | `PLAYBOOK.md:131` ("session-count/weekly time budget... pure logistics"); `program.md:18-19` (frequency null at matched volume) | Existing |
| **More time, want more** | Add sets to the four primary compounds (1-1a/2-1b/3-1/4-1) only, up to the ~20 set/wk plateau | Adding new exercises (14th+), or raising frequency further | `program.md:102` ("add a set... rather than new exercises"); `program.md:9` (returns flatten past ~20) | Existing |
| **Stalled on one lift** | Run the 5-step sequence above; if it survives steps 1-4 *and* the situation meets `loop.md:111`'s evidence-triggered bar (a documented pain/joint-comfort issue, not "it stopped progressing"), use *that lift's* pre-approved fixed sub only | Swap the exercise immediately on the assumption a stall means the wrong exercise, or add RIR as a "recovery" concession | `loop.md:111` (governs performance/pain-triggered substitution — corrected; a prior draft mis-applied `exercises.md`'s friction/dread test here, which governs a *different* complaint, used correctly below for RDL/BSS discomfort specifically) | Corrected this pass; sequence is new synthesis |
| **Stalled everywhere at once** | Same 5-step sequence, but step 2 (calories) is usually decisive at near-maintenance intake | Adding volume across the board | `program.md:192` — the repo already states this exact wrong-knob warning verbatim ("the fix is +150 kcal, not +5 sets") | Existing (citation line corrected this pass) |
| **Gym lacks a piece of equipment (station occupied)** | Use the one pre-approved fixed substitute for that slot | Improvising a different exercise "for now" | `program.md:122-136` (fixed-sub table), `program.md:118-120` (busy-gym rule, anti-rationalization line) | Existing |
| **Gym permanently lacks equipment (doesn't own it, not just busy)** | Re-run that slot through `exercises.md`'s 5-criteria framework from scratch — the fixed-sub table assumes a "busy but well-equipped" gym, not a missing category of machine | Treating the fixed sub as a permanent primary without re-checking it against the 5 criteria for *your* gym | `program.md:197` ("busy but well-equipped" is a stated input, not a universal); `PLAYBOOK.md:132` ("Gym equipment access... don't import this repo's answer if you don't lift at the same gym") | New — repo's sub table is scoped to logistics/contention, not to genuine absence |
| **Something hurts (sharp/joint pain)** | Swap that slot's fixed sub immediately (pre-vetted growth-equivalent, so zero stimulus cost); if pain persists on the sub too, stop and get it assessed — outside program scope | Pushing to failure "through it" (no reason to — failure ≈ 1-2 RIR anyway), or abandoning the whole program instead of one slot | `program.md:10` (failure buys ~nothing over 1-2 RIR, so there's no reason to grind); `loop.md:111` (substitution "evidence-triggered only... e.g. a documented pain/joint-comfort issue") | Existing for the swap; assessment step is new (not in repo — genuinely out of scope) |
| **Something is *uncomfortable* but not painful (RDL/BSS deep-stretch positions)** | Distinguish before reaching for any knob: does it target the near-failure sets or the loaded-stretch position itself? If yes, that's the stimulus, not a cost — no swap | Reclassifying discomfort as "pain" to justify a swap | `exercises.md:43` (anti-rationalization sharper test, explicit for RDL/BSS) | Existing |
| **Want to cut now** | If proceeding anyway: bump protein to 130-190 g/day, track skinfold mm not %BF, expect blunted lean gain, keep sets/RIR unchanged through the cut, deload trigger gets touchier in a deficit (recovery capacity drops) | Cutting to a target %BF for "visible abs" — no such threshold exists at any measurement method | `abs.md:92,96-100`; `AGENTS.md:38` (sequencing ruling); `abs.md:84` (ES −0.57 lean-gain blunting) | Existing for sequencing/protein; "keep training variables unchanged, deload gets touchier" is new — repo never states a training-side adjustment for a cut |
| **New scan, surprising number** | Re-run `PLAYBOOK.md` steps 1-2 on it: trace to measured (weight/impedance) vs derived (PBF/SMM), check the delta against the ~±2-4 point PBF noise floor before treating it as signal | Changing volume, cutting, or swapping exercises off a single scan | `AGENTS.md:26`, `scans/scans.md:7,10`, `program.md:194-197` | Existing |
| **Bored (mid-block)** | Use the free-choice slots (lateral raise DB/cable, curl standing/incline) and the built-in set-structure variety (myo-reps, drop-sets) | Swapping compounds for novelty, or increasing exercise count | `exercises.md:45` (novelty explicitly excluded as a decision criterion); `program.md:108-114` | Existing |
| **Bored (whole program, after a full block)** | Full re-run of `exercises.md`'s 5-criteria selection, no more often than the 6-12 week minimum-hold floor | Rotating exercises every few weeks "to keep it interesting" | `program.md:158` (6-12+ week floor is the only stated constraint); no explicit refresh cadence exists | New — repo names the floor, never names a ceiling/refresh trigger |
| **Missed 1 week** | Resume at last logged weights, normal RIR, for every lift except the RDL | Restarting the full return-to-training ramp reflexively | Mechanism is tendon-load-tolerance lag (`program.md:162-166`), *not* the muscle-maintenance curve — the 32-week maintenance data (`program.md:162`) answers whether muscle size is held, not whether tendon load tolerance regresses in a week, a different question. A week is far shorter than the 1-3 week windows the doc already uses for tendon adaptation, so "probably fine" is an extrapolation, not a citation. | New — corrected this pass; the prior draft cited the muscle-maintenance curve for what is actually a tendon question |
| **Missed 2 weeks** | One light session (RIR 3, ~90% prior load) on the compounds generally; treat the RDL per its own exception — start it at RIR 3-4 for one session rather than cold at RIR 2, since it already gets 3x the ramp of everything else even from a fresh start | Full 3-week ramp on everything, or resuming cold at prior RIR 1-2 on the RDL specifically | Same tendon-lag mechanism (`program.md:162-166`), scaled down for a shorter absence — explicitly a judgment call, not literature-sourced | New — corrected this pass (mechanism), and now threads the RDL exception through explicitly, which the prior draft didn't |
| **Missed a month** | Compressed ramp: ~1 week at RIR 3-4 on everything; RDL gets roughly 2 weeks (RIR 4→3), scaling its documented 3x sensitivity rather than reusing the general 1-week number | Either the full return-to-training ramp (over-cautious) or resuming cold at working weights (under-cautious, risks the tendon-lag injury mechanism) | Extrapolated from `program.md:160-176`'s core finding (muscle lags loss, tendon lags load-tolerance) at a shorter timescale, scaled per-lift | Explicitly a judgment call, not literature-sourced like the original ramp — now scales the RDL exception proportionally instead of treating the ramp as one number |

### Notes on the asymmetry this map respects

Every "correct knob" column above reaches for a growth-neutral variable first (exercise choice within a slot, split, frequency, session count, set-structure) and only touches weekly sets, RIR, or progressive overload when the situation is genuinely about those three (more time → add sets to compounds; stalled everywhere → check calories before volume). No situation's correct answer is "reduce RIR as a convenience" or "cut sets below the stated per-muscle target without a deload trigger" — those are the two ways a friction fix quietly becomes a stimulus cut (`exercises.md:11`).
